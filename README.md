# Data_Pivot_Tool

GUI for Pivoting data from Horizontal to Vertical format.

Steps for use:

  1.) using menu buttons, select Load and select the file can be in either .xlsx or .csv format.
  2.) in bottom left, select columns that correspond to key fields. every column not selected with be pivoted on.
  3.) the buttoms at the very bottom right are to remove unnessary data and reduce final file size
    Remove: will remove any string value that matches what is typed in this field
    :0 Remove all 0 values
    :NULL remove all np.Nan / null values
    :- remove "-" values if those are being used as placeholders
    :* remove "*" values if those are being used as placeholders
    :Duplicates remove any duplicate rows, all values must be identical to be removed by this function
  4.) hit preview from the menu buttons to preview converted output
  5. hit Extract to open the file save dialogue and select a file to save the converted data to
