# dsview-spi-merge
Quick and dirty script to merge exported data from DSView into a single file for analysis

# Usage
./dsview-spi-merge export1.txt export2.txt -o output.txt

- export1/export2 can be either MOSI or MISO but both files are required to merge

# Sample Output
```
# Merge of:
# MOSI File: decoder--220330-170606-MOSI.txt
# MISO File: decoder--220330-170606.txt

---ID--- - Dir  - --------Delta     (ns)--------  - --Data--

       0 - MOSI -                               0 - 30 70 F0 00 00 00 00
       0 - MISO -                               0 - 00 00 00 00 00 00 00

       1 - MOSI -                          414700 - 31 70 F0 00 00 00 20
       1 - MISO -                          414700 - 00 00 00 00 00 00 00

       2 - MOSI -                          406180 - 30 70 F0 00 00 00 00
       2 - MISO -                          406180 - 00 00 00 00 00 00 00

       3 - MOSI -                         5781080 - 31 70 F0 00 00 00 03
       3 - MISO -                         5781080 - 00 00 00 00 00 00 00
```

