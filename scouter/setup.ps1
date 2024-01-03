Param(
    [Parameter(Mandatory=$True,Position=1)]
    [string]$dbfile,
    
    [Parameter(Mandatory=$True,Position=2)]
    [string]$tba
)
# rm scoutingTest.sqlite3
python cli.py create --file $dbfile
python cli.py schedule --set --tba $tba
python cli.py teams --set --tba $tba