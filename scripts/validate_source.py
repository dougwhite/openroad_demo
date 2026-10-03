"""Validate demo source without OpenROAD, connections or cached native XML."""

import json
import shutil
import tempfile
from pathlib import Path

from lxml import etree

from gorak.component_defaults import encode_source_w4gl, write_component_defaults
from gorak.contract_source import equivalent
from gorak.export import application_metadata, apply_field_default_inheritance
from gorak.parser import parse_application_xml, parse_component_node, parse_w4gl
from gorak.portable_source import restore_application, restore_component
from gorak.xml_writer import document


def validate(root: Path) -> None:
    applications = sorted(root.glob("*/app.json"))
    if not applications:
        raise ValueError("No applications found")
    count = 0
    with tempfile.TemporaryDirectory(prefix="gorak-demo-validation-") as temporary:
        target = Path(temporary)
        shutil.copyfile(root / "field_defaults.json", target / "field_defaults.json")
        for metadata in applications:
            folder = metadata.parent
            output = target / folder.name
            output.mkdir()
            shutil.copyfile(metadata, output / "app.json")
            styles = folder / "field_defaults.json"
            if styles.exists():
                shutil.copyfile(styles, output / styles.name)
            # Serialize and parse native XML too, exercising the actual wire format.
            native_app = etree.fromstring(document([restore_application(folder)]))
            parsed_app = parse_application_xml(native_app)
            projected = application_metadata(
                parsed_app.application,
                included_applications=parsed_app.included_applications,
            )
            original = json.loads(metadata.read_text(encoding="utf-8"))
            if projected != original:
                raise ValueError(
                    f"Application metadata changed: {metadata.relative_to(root)}"
                )
            sources = sorted(folder.glob("*.w4gl"))
            if not sources:
                raise ValueError(f"No components in {folder.name}")
            for markup in folder.glob("*.wml"):
                if not markup.with_suffix(".w4gl").exists():
                    raise ValueError(f"Orphan WML: {markup.relative_to(root)}")
            for source in sources:
                native = etree.fromstring(document([restore_component(source)])).find(
                    "COMPONENT"
                )
                if native is None:
                    raise ValueError(f"Missing native component: {source.name}")
                component = parse_component_node(native)
                apply_field_default_inheritance(
                    target, folder.name, [component], source_nodes=[native]
                )
                destination = output / source.name
                text = encode_source_w4gl(component)
                destination.write_text(text, encoding="utf-8", newline="\n")
                # TOML formatting may canonicalize; metadata and script must survive.
                if parse_w4gl(
                    source.read_text(encoding="utf-8"), source.stem
                ) != parse_w4gl(text, source.stem):
                    raise ValueError(f"W4GL changed: {source.relative_to(root)}")
                if component.markup is not None:
                    parser = etree.XMLParser(
                        resolve_entities=False, no_network=True, remove_blank_text=True
                    )
                    before = etree.fromstring(
                        source.with_suffix(".wml").read_bytes(), parser
                    )
                    after = etree.fromstring(component.markup.encode("utf-8"), parser)
                    if etree.tostring(before, method="c14n") != etree.tostring(
                        after, method="c14n"
                    ):
                        raise ValueError(f"WML changed: {source.relative_to(root)}")
                    destination.with_suffix(".wml").write_text(
                        component.markup, encoding="utf-8", newline="\n"
                    )
                    write_component_defaults(
                        destination, component.props["fielddefaults"]
                    )
                if not equivalent(native, restore_component(destination)):
                    raise ValueError(
                        f"Native round trip changed: {source.relative_to(root)}"
                    )
                count += 1
    print(f"Validated {len(applications)} applications and {count} components")


if __name__ == "__main__":
    validate(Path(__file__).resolve().parent.parent)
