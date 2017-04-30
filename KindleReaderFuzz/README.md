# KindleReaderFuzz
Fuzzer created to fuzz kindle reader for PC. Test cases were created seperately, fuzzer opens file checks for crash if it does not crash after loading it selects file and tries to read it to check for crash. Windbg is attached while it runs, report will be produced from Windbg and written to a file.
