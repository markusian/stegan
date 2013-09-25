stegan
======

A simple stegranography application for hiding messages inside images

This program encrypts and decrypts a message inside an
    image using steganography.

    Use --help or -h for details on usage
    
    In encrypt mode:
        The message is transformed in a sequence of bits, preceded by a
        fixed length 16 bits sequence that represents the length of the
        message to be hidden.
        The bit sequence is then encoded in the least significant bits
        of the blue component of the image. The image is then stored
        in the same folder, using the name of the original file preceded by
        "encrypted_".
        As the length of the message has to be encoded in 16 bits, only 
        messages that can be encoded in 2^16=65536 bits are allowed
        
    In decrypt mode:
        The list of all the least significant bits of the blue component of
        the given image is considered.
        Then the first 16 bits are interpreted as the lenght of the following
        hidden message.
        Then, the hidden message is shown to screen

        N.B. the program is not robust to decryption of images that have 
        not been built with this program  
