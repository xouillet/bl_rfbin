import binascii
import fdt


def little_endian(data):
    return binascii.hexlify(binascii.unhexlify(data)[::-1]).decode("utf-8")


def bl_dts2hex(dts):
    with open(dts, "r", encoding="utf-8") as (f):
        tmp_dts = f.read()
    fdt_obj = fdt.parse_dts(tmp_dts)
    xtal_mode = fdt_obj.get_property("xtal_mode", "wifi/brd_rf")
    xtal = fdt_obj.get_property("xtal", "wifi/brd_rf")
    pwr_mode = fdt_obj.get_property("pwr_mode", "wifi/brd_rf")
    pwr_offset = fdt_obj.get_property("pwr_offset", "wifi/brd_rf")
    pwr_table_11b = fdt_obj.get_property("pwr_table_11b", "wifi/brd_rf")
    pwr_table_11g = fdt_obj.get_property("pwr_table_11g", "wifi/brd_rf")
    pwr_table_11n = fdt_obj.get_property("pwr_table_11n", "wifi/brd_rf")
    en_tcal = fdt_obj.get_property("en_tcal", "wifi/rf_temp")
    linear_or_follow = fdt_obj.get_property("linear_or_follow", "wifi/rf_temp")
    tchannels = fdt_obj.get_property("Tchannels", "wifi/rf_temp")
    tchannel_os = fdt_obj.get_property("Tchannel_os", "wifi/rf_temp")
    tchannel_os_low = fdt_obj.get_property("Tchannel_os_low", "wifi/rf_temp")
    troom_os = fdt_obj.get_property("Troom_os", "wifi/rf_temp")
    pwr_table_ble = fdt_obj.get_property("pwr_table_ble", "bluetooth/brd_rf")
    init_hex = little_endian(bytes("k1bXkD6O", encoding="ascii").hex())
    if xtal_mode:
        length = "%02x" % len(xtal_mode[0])
        xtal_mode_hex = (
            "0100" + length + "00" + bytes(xtal_mode[0], encoding="ascii").hex()
        )
    else:
        xtal_mode_hex = ""
    if xtal:
        xtal_hex = "02001400"
        for item in xtal:
            item_hex = little_endian("%08x" % item)
            xtal_hex += item_hex

    else:
        xtal_hex = ""
    if pwr_mode:
        length = "%02x" % len(pwr_mode[0])
        pwr_mode_hex = (
            "0300" + length + "00" + bytes(pwr_mode[0], encoding="ascii").hex()
        )
    else:
        pwr_mode_hex = ""
    if pwr_table_11b:
        pwr_table_11b_hex = "05000400"
        for item in pwr_table_11b:
            item_hex = "%02x" % item
            pwr_table_11b_hex += item_hex

    else:
        pwr_table_11b_hex = ""
    if pwr_table_11g:
        pwr_table_11g_hex = "06000800"
        for item in pwr_table_11g:
            item_hex = "%02x" % item
            pwr_table_11g_hex += item_hex

    else:
        pwr_table_11g_hex = ""
    if pwr_table_11n:
        pwr_table_11n_hex = "07000800"
        for item in pwr_table_11n:
            item_hex = "%02x" % item
            pwr_table_11n_hex += item_hex

    else:
        pwr_table_11n_hex = ""
    if pwr_offset:
        pwr_offset_hex = "08000e00"
        for item in pwr_offset:
            item_hex = "%02x" % item
            pwr_offset_hex += item_hex

    else:
        pwr_offset_hex = ""
    if en_tcal:
        en_tcal_hex = "20000100%02x" % en_tcal[0]
    else:
        en_tcal_hex = ""
    if linear_or_follow:
        linear_or_follow_hex = "21000100%02x" % linear_or_follow[0]
    else:
        linear_or_follow_hex = ""
    if tchannels:
        tchannels_hex = "22000a00"
        for item in tchannels:
            item_hex = little_endian("%04x" % item)
            tchannels_hex += item_hex

    else:
        tchannels_hex = ""
    if tchannel_os:
        tchannel_os_hex = "23000a00"
        for item in tchannel_os:
            item_hex = little_endian("%04x" % item)
            tchannel_os_hex += item_hex

    else:
        tchannel_os_hex = ""
    if tchannel_os_low:
        tchannel_os_low_hex = "24000a00"
        for item in tchannel_os_low:
            item_hex = little_endian("%04x" % item)
            tchannel_os_low_hex += item_hex

    else:
        tchannel_os_low_hex = ""
    if troom_os:
        troom_os_hex = "25000200" + little_endian("%04x" % troom_os[0])
    else:
        troom_os_hex = ""
    if pwr_table_ble:
        pwr_table_ble_hex = "30000400" + little_endian("%08x" % pwr_table_ble[0])
    else:
        pwr_table_ble_hex = ""
    dts_hex = (
        init_hex
        + xtal_mode_hex
        + xtal_hex
        + pwr_mode_hex
        + pwr_table_11b_hex
        + pwr_table_11g_hex
        + pwr_table_11n_hex
        + pwr_offset_hex
        + en_tcal_hex
        + linear_or_follow_hex
        + tchannels_hex
        + tchannel_os_hex
        + tchannel_os_low_hex
        + troom_os_hex
        + pwr_table_ble_hex
    )
    print(dts_hex)
    return bytearray.fromhex(dts_hex)

def merge(input, b, output):
    with open(input, 'rb') as i:
        ba = bytearray(i.read())
        ba[1032:1032 + len(b)] = b

    output.write(ba)


if __name__ == "__main__":
    import sys
    _, input, dts = sys.argv

    with open('out', 'wb') as output:
        merge(input, bl_dts2hex(dts), output)

