name=XPS15-9550
root=$(dirname $0)/.. 
# python $root/update.py --set $(sh $root/Script/gen_sn_mlb_uuid.sh)
# random one
python $root/update.py $1 --set sn=C02VK0ZLGTFN mlb=C02742306QXHCF9JC smuuid=C167D3A2-CC13-4041-8CED-553D772C0749
cd $root && zip -r ${name}-$1-$(date +%y%m).zip $1 Tool Script README.md Changelog.md update.py packages.csv