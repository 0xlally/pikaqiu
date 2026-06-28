# Professional 1.7.11

Source: https://portswigger.net/burp/releases/professional-1-7-11
Fetched: 2026-06-28T09:16:28.478282+00:00

This release adds support for the .NET platform in the Burp Infiltrator tool.

To use Burp Infiltrator on .NET applications, go to Burp menu / Burp Infiltrator, and select the .NET option in the export wizard. For more details, see the Burp Infiltrator documentation.

The new .NET version of Burp Infiltrator works in the same way as the existing Java version. It supports languages written in C#, VB, and any other .NET languages. It supports versions 2.0 and later of the .NET framework.

To patch .NET applications, Burp Infiltrator makes use of bytecode assembly and disassembly tools. These can be either: (a) the ilasm and ildasm tools that are distributed with the .NET framework and the Windows SDK tools, respectively; or (b) the ilasm and monodis tools that are distributed with mono. You must specify the location of the assembly and disassembly tools during the patching process. Note that the version of the assembly tool must match the version of the .NET framework that the bytecode is targeting, to ensure compatibility.
