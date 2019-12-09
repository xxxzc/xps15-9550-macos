root=$(dirname $0)/.. 
package=macinfo-2.0.9-mac.zip
macserial=$root/Tool/macserial
if [ ! -f $macserial ]; then
    echo macserial not exist, downloading...
    curl -LOk https://github.com/acidanthera/MacInfoPkg/releases/download/2.0.9/$package
    unzip $package macserial -d $root/Tool && rm -rf $package
    chmod a+x $macserial
fi
read sn s mlb <<< $($macserial -m MacBookPro13,3 -g -n 1)
echo sn=$sn mlb=$mlb smuuid=$(uuidgen)
