# UnitTestFramework

`unittestframework/` contains the OpenROAD UnitTestFramework used by this demo.
Its source comments credit Bodo Bergmann; those comments are retained. The source
was recovered from a retained XML export of the installed framework and encoded
using current Gorak's compact readable format. Trailing whitespace and mixed
indentation were normalized; framework behavior was not changed. No database identities, XML cache,
compiled images or credentials are included.

The exported application contains no standalone license text or version number.
The root MIT license applies to the original demo and does not relicense this
third-party source. Consult the framework's original distribution for its terms.

The framework includes a Windows `GetTickCount64` declaration in `kernel32.dll`.
The OpenROAD runtime must be able to load that library. Only the Launch Score
suite is registered in `gorak.json`; the framework's sample suite is not run by
bare `gorak test`.
