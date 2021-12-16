def parse_input(input_filename):
    with open(input_filename) as f:
        return f.read().strip()


def hex_to_binary(hex):
    return str(bin(int('1' + hex, 16)))[3:]


def bits_to_decimal(bits):
    num = 0
    for i, b in enumerate(reversed(bits)):
        num += (2**i)*int(b)
    return num


def parse_literal(string):
    literal = ""
    head = string[:5]
    while head[0] != '0':
        string = string[5:]
        literal += head[1:]
        head = string[:5]
    string = string[5:]
    literal += head[1:]

    return literal, string


def parse_operator(string):
    length_type_id, string = string[0], string[1:]
    if length_type_id == '0':
        length_in_bits, string = string[:15], string[15:]
        length = bits_to_decimal(length_in_bits)
        sub_packets_string, remainder = string[:length], string[length:]
        sub_packets, _ = parse_sub_packets(sub_packets_string)
    else:
        total_packets_in_bits, string = string[:11], string[11:]
        total_number_of_packets = bits_to_decimal(total_packets_in_bits)
        sub_packets, remainder = parse_sub_packets_by_count(string, total_number_of_packets)

    return sub_packets, remainder


def parse_sub_packets(string):
    sub_packets = []
    while string:
        packet, string = parse_packet(string)
        sub_packets.append(packet)

    return sub_packets, string


def parse_sub_packets_by_count(string, total_number_of_packets):
    sub_packets = []
    while len(sub_packets) < total_number_of_packets:
        packet, string = parse_packet(string)
        sub_packets.append(packet)

    return sub_packets, string


def parse_packet(string):
    version, type, string = string[:3], bits_to_decimal(string[3:6]), string[6:]
    packet = {'version': version, 'type': type}
    if type == 4:
        literal, string = parse_literal(string)
        packet['literal'] = bits_to_decimal(literal)
    else:
        sub_packets, string = parse_operator(string)
        packet['sub_packets'] = sub_packets
    return packet, string


def sum_versions(packet_tree):
    version = bits_to_decimal(packet_tree['version'])
    if 'sub_packets' not in packet_tree:
        return version
    else:
        return version + sum(sum_versions(sub_packet) for sub_packet in packet_tree['sub_packets'])


def eval_packet(packet):
    if packet['type'] == 0:
        return sum(eval_packet(p) for p in packet['sub_packets'])
    elif packet['type'] == 1:
        prod = 1
        for p in packet['sub_packets']:
            prod *= eval_packet(p)
        return prod
    elif packet['type'] == 2:
        return min(eval_packet(p) for p in packet['sub_packets'])
    elif packet['type'] == 3:
        return max(eval_packet(p) for p in packet['sub_packets'])
    elif packet['type'] == 4:
        return packet['literal']
    elif packet['type'] == 5:
        return 1 if eval_packet(packet['sub_packets'][0]) > eval_packet(packet['sub_packets'][1]) else 0
    elif packet['type'] == 6:
        return 1 if eval_packet(packet['sub_packets'][0]) < eval_packet(packet['sub_packets'][1]) else 0
    elif packet['type'] == 7:
        return 1 if eval_packet(packet['sub_packets'][0]) == eval_packet(packet['sub_packets'][1]) else 0


def analyze_packet(packet):
    sum_of_versions = sum_versions(packet)
    value = eval_packet(packet)
    return sum_of_versions, value


def test_code():
    test_inputs_part1 = [("C0015000016115A2E0802F182340", 23), ("620080001611562C8802118E34", 12), ("8A004A801A8002F478", 16), ("A0016C880162017C3686B18A3D4780", 31)]
    for hexinput, expected in test_inputs_part1:
        binary = hex_to_binary(hexinput)
        packet = parse_packet(binary)[0]
        sum_of_versions = sum_versions(packet)
        # print(f"{hexinput}: {sum_of_versions}, expected: {expected}")
        assert sum_of_versions == expected

    test_inputs_part2 = [("C200B40A82", 3), ("04005AC33890", 54), ("880086C3E88112", 7), ("CE00C43D881120", 9), ("D8005AC2A8F0", 1), ("F600BC2D8F", 0), ("9C005AC2F8F0", 0), ("9C0141080250320F1802104A08", 1)]
    for hexinput, expected in test_inputs_part2:
        binary = hex_to_binary(hexinput)
        packet = parse_packet(binary)[0]
        value = eval_packet(packet)
        # print(f"{hexinput}: {value}, expected: {expected}")
        assert value == expected


test_code()
hexinput = parse_input('16input')
binary = hex_to_binary(hexinput)
packet, remainder = parse_packet(binary)
sum_of_versions, value = analyze_packet(packet)
print(f"{hexinput}")
print(f"Sum of versions: {sum_of_versions}")
print(f"Packet value: {value}")
