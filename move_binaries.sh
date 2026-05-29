#!/bin/bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo ""
echo "Downloading insta 360 binaries..."
echo ""

git clone git@github.com:RPL-CS-UCL/insta360_binaries.git

echo ""
echo "Unzipping files..."
echo ""

cd insta360_binaries
git lfs pull
unzip Linux_CameraSDK-2.1.1_MediaSDK-3.1.1.zip

architecture=""
case $(uname -m) in
    i386)   architecture="386" ;;
    i686)   architecture="386" ;;
    x86_64) architecture="amd64" ;;
    aarch64) architecture="arm64" ;;
    arm)    dpkg --print-architecture | grep -q "arm64" && architecture="arm64" || architecture="arm" ;;
esac

echo "architecture: $architecture"

target_dir=""
unziped_dir=""
if [ "$architecture" = "amd64" ]; then
  target_dir="CameraSDK-2.1.1-Linux.tar.gz"
  unzipped_dir="CameraSDK-20251104_115504-2.1.1.1-Linux"
elif [ "$architecture" = "arm64" ] && \
  grep -q "Jetson" /sys/firmware/devicetree/base/model; then
  target_dir="CameraSDK-2.1.1-jetson-linux-9.3.0-2020.08-x86_64_aarch64_linux-gnu.tar.gz"
  unzipped_dir="CameraSDK-20251105_112855-2.1.1-jetson-linux-9.3.0-2020.08-x86_64_aarch64_linux-gnu"
elif [ "$architecture" = "arm64" ]; then
  target_dir="CameraSDK-2.1.1-gcc-arm-11.2-2022.02-x86_64-aarch64-none-linux-gnu.tar.gz"
  unzipped_dir="CameraSDK-20251105_140609-2.1.1-gcc-arm-11.2-2022.02-x86_64-aarch64-none-linux-gnu"
else
  echo -e "Can't find architecture"
  exit 1
fi

echo "target dir: $target_dir"

tar -xzf ./Linux_CameraSDK-2.1.1_MediaSDK-3.1.1/$target_dir

cp -r ./$unzipped_dir/include/. ../include
cp -r ./$unzipped_dir/lib/. ../lib

cd ..

echo ""
echo "Done, moved binaries to environments are kept in 'insta360_ros_driver/lib' and headers to 'insta360_ros_driver/include'."
echo ""
