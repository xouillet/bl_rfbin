# bl_rfbin

bl_rfbin is a small utility that will embed RF parameters for the Bouffalo BL602 from a dts file
prior to flash.

It is useful if you want to flash `nuttx` binary using `blflash` or another third-party tool (cf https://github.com/apache/incubator-nuttx/issues/4336).

The code is reversed engineered from the official BouffaloLabDevCube.

## Usage

```
usage: bl_rfbin.py [-h] input dts output

positional arguments:
  input       binary file to patch
  dts         dts file for board
  output      output file (use - for stdout)

optional arguments:
  -h, --help  show this help message and exit
```

For example:

```
python bl_rfbin.py ../nuttx/nuttx.bin ../bl_iot_sdk/tools/flash_tool/bl602/device_tree/bl_factory_params_IoTKitA_40M.dts out.bin
```

Or chainloading with blflash

```
python bl_rfbin.py ../nuttx/nuttx.bin ../bl_iot_sdk/tools/flash_tool/bl602/device_tree/bl_factory_params_IoTKitA_40M.dts - | blflash flash /dev/stdin --port /dev/ttyUSB0
```
