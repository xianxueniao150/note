set -x
set -e

basepath=$(cd `dirname $0`; pwd)

echo ${basepath}

# pacman -S nasm -y

cd ${basepath}/ffmpeg
pwd

NDK=/home/master/download/android-ndk-r23b
TOOLCHAIN=$NDK/toolchains/llvm/prebuilt/linux-x86_64

function build_android
{

echo "开始编译 $CPU"

./configure \
    --prefix=${basepath}/ffmpeg_android_install \
    --enable-static \
    --enable-shared \
    --enable-cross-compile \
    --target-os=android \
    --arch=$ARCH \
    --cc=$CC \
    --cross-prefix=$CROSS_PREFIX \
    --enable-ffmpeg \
    --disable-ffplay \
    --disable-ffprobe \
    --disable-avdevice \
    --disable-doc \
    --disable-symver \
    --enable-gpl   

make clean
make -j8
make install


echo "编译成功 $CPU"

}

export AR=$TOOLCHAIN/bin/llvm-ar
export AS=$CC
export RANLIB=$TOOLCHAIN/bin/llvm-ranlib
export STRIP=$TOOLCHAIN/bin/llvm-strip


# #这里注意 32位和64位不一样
# export LD=$TOOLCHAIN/bin/ld
# #armv7-a
# ARCH=arm
# CPU=armv7-a
# API=21
# CC=$TOOLCHAIN/bin/armv7a-linux-androideabi$API-clang
# CROSS_PREFIX=$TOOLCHAIN/bin/llvm-

# build_android

export LD=$TOOLCHAIN/bin/ld64

#armv8-a
ARCH=arm64
CPU=armv8-a
API=21
CC=$TOOLCHAIN/bin/aarch64-linux-android$API-clang
CROSS_PREFIX=$TOOLCHAIN/bin/llvm-

build_android
