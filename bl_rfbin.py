import argparse
import fdt
import logging
import sys

logger = logging.getLogger(__name__)

RFPA_OFFSET = 0x400
RFPA_MAGIC = b"BLRFPARA"


def dts2tlv(dts):

    with open(dts, "r") as dts_f:
        fdt_obj = fdt.parse_dts(dts_f.read())

    def tlv(type, name, path, word_size=1):
        """
        type is the type in the final tlv
        name and path are the same as fdt_obj.get_property
        word_size set the word size of single element
        """

        out = bytearray()
        try:
            obj = fdt_obj.get_property(name, path)
        except ValueError:
            return out

        out += type.to_bytes(2, "little")
        if isinstance(obj, fdt.items.PropStrings):
            out += len(obj[0]).to_bytes(2, "little")
            out += bytes(obj[0], "ascii")
        elif isinstance(obj, fdt.items.PropWords):
            if len(obj) > 1:
                out += (len(obj) * word_size).to_bytes(2, "little")
                for elem in obj:
                    out += elem.to_bytes(word_size, "little")
            else:
                out += word_size.to_bytes(2, "little")
                out += obj[0].to_bytes(word_size, "little")

        return out

    out = bytearray(b"O6DkXb1k")  # init magic
    out += tlv(0x1, "xtal_mode", "wifi/brd_rf")
    out += tlv(0x2, "xtal", "wifi/brd_rf", word_size=0x4)
    out += tlv(0x3, "pwr_mode", "wifi/brd_rf")
    out += tlv(0x5, "pwr_table_11b", "wifi/brd_rf")
    out += tlv(0x6, "pwr_table_11g", "wifi/brd_rf")
    out += tlv(0x7, "pwr_table_11n", "wifi/brd_rf")
    out += tlv(0x8, "pwr_offset", "wifi/brd_rf")
    out += tlv(0x20, "en_tcal", "wifi/rf_temp")
    out += tlv(0x21, "linear_or_follow", "wifi/rf_temp")
    out += tlv(0x22, "Tchannels", "wifi/rf_temp", word_size=0x2)
    out += tlv(0x23, "Tchannel_os", "wifi/rf_temp", word_size=0x2)
    out += tlv(0x24, "Tchannel_os_low", "wifi/rf_temp", word_size=0x2)
    out += tlv(0x25, "Troom_os", "wifi/rf_temp", word_size=0x2)
    out += tlv(0x30, "pwr_table_ble", "bluetooth/brd_rf", word_size=0x4)

    logger.debug(out.hex())
    return out


def patch(input, dts, output):
    with open(input, "rb") as f_i:
        ba = bytearray(f_i.read())

    tlv_offset = RFPA_OFFSET + len(RFPA_MAGIC)
    if ba[RFPA_OFFSET:tlv_offset] != RFPA_MAGIC:
        logger.error("Input file doesn't support patching")
        sys.exit(1)

    tlv = dts2tlv(dts)
    ba[tlv_offset : tlv_offset + len(tlv)] = tlv

    if output == '-':
        sys.stdout.buffer.write(ba)
    else:
        with open(output, "wb") as f_o:
            f_o.write(ba)


if __name__ == "__main__":

    logging.basicConfig()

    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="binary file to patch")
    parser.add_argument("dts", help="dts file for board")
    parser.add_argument("output", help="output file (use - for stdout)")

    args = parser.parse_args()
    patch(args.input, args.dts, args.output)
