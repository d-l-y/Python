# URLfuzzhttps://github.com/d-l-y/Python/tree/master/URLfuzzer
Python script to quickly fuzz a broad scope of URLs with user defined input

I use this to fuzz a large number of URLs with payloads I can define and grep for reflections I define(xss,sql errors,sensitve data). Typically I spider many sites within a scope in Burpsuite and copy the URLs to my url list input file.
meant to be simple quick and easily modified for the use I need.

`Usage: python urlfuzz27.py <URL list input file>`
