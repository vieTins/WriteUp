#include <iostream>
#include <cstring>
#include <cstdint>

// encrypted flag 
uint8_t encrypted_flag[56] = {
    0x56, 0x9d, 0xb3, 0x85, 0xaf, 0x7f, 0xa0, 0x4b,
    0x83, 0x49, 0x76, 0xe0, 0x21, 0x78, 0x22, 0xed,
    0x0e, 0xd9, 0xfd, 0xf5, 0xb8, 0xb8, 0xd8, 0x1a,
    0x16, 0x93, 0x70, 0x07, 0x35, 0x34, 0x27, 0xc5,
    0x34, 0xba, 0x09, 0x74, 0xda, 0x68, 0xe8, 0x7e,
    0x6c, 0x8b, 0x9b, 0x83, 0x00, 0x00, 0x00, 0x00
};

// XOR key 
uint8_t xor_key[20] = {
    0x84, 0xdb, 0xaf, 0xf2, 0x4e, 0xd0, 0xad, 0x20,
    0xd7, 0xa0, 0x18, 0xd7, 0x15, 0x52, 0x51, 0x7b,
    0x5b, 0x14, 0x26, 0xd1
};

// rotate function
uint8_t rol8(uint8_t value, uint8_t shift) {
    return ((value << (shift & 0x1F)) | (value >> ((8 - shift) & 0x1F))) & 0xFF;
}

// encrypt function
void start_crypt(const char* input, uint8_t* output) {
    size_t len = strlen(input);
    for (size_t i = 0; i < len; i++) {
        uint8_t b1 = input[i];
        uint8_t b2 = xor_key[(i * 7) % 20];
        uint8_t b3 = rol8(xor_key[i % 20], (i * 3) & 7);
        uint8_t shift = i % 5;
        output[i] = b1 ^ b3 ^ (b2 >> shift);
    }
}

// Function to check the flag
bool check_flag(const char* input) {
    size_t len = strlen(input);
    if (len != 44) {  
        return false;
    }

    uint8_t result[56] = {0};
    start_crypt(input, result);
    return memcmp(result, encrypted_flag, 44) == 0;
}

// main 
int main() {
    std::string flag;
    std::cout << "Enter flag: ";
    std::getline(std::cin, flag);

    if (check_flag(flag.c_str())) {
        std::cout << "Correct flag!\n";
    } else {
        std::cout << "Wrong flag!\n";
    }

    return 0;
}

// I rewrite the code from IDA 