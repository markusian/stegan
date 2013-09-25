#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: ferdinando papale, s121035
"""

import argparse
import Image
import bitarray

class LongMessageException(Exception):
    """
        Thrown when the message is too long to be encrypted
    """
    pass

       
class NoMessageException(Exception):
    """
        Thrown when the user doesn't supply a message to encrypt
    """
    pass
      
class SmallImageException(Exception):
    """
        Thrown when the image is not big enough to contain the specified 
        message
    """
    pass


def encrypt(image, message):
    """
        This function encrypts the given message in the image.
        In order to do so, the message is transformed in a sequence of bits,
        of which the first 16 represent the legth of the hidden message.
        Then, row-wise, the least significant byte of the blue component
        of the image is modified according to the sequence of bits.
    
    """
    x,y = image.size
    bit_message = to_bits(message)
    
    if len(bit_message) > x*y:
        raise SmallImageException()

    mat = image.load()
    count = 0
    done = False
    for i in range(x):
        for j in range(y):
            mat[i,j] = (mat[i,j][0],mat[i,j][1],sub(mat[i,j][1],int(bit_message[count])))
            count = count + 1
            if count == len(bit_message):
                done = True
                break
        if done:
            break

def decrypt(image):   
    """
        This function return the decrypted the message from the given image. 
    
    """
    x,y = image.size
    mat = image.load()
    bits = ''.join(['0' if mat[i,j][2]%2==0 else '1'  for i in range(x) for j in range(y)])
    return from_bits(bits)
    
def to_bits(message):
    """
        This function returns a string of bits that needs to be hidden 
        in the image.
        The first 16 bits encrypted in the image represent the length (in 
        bits) of the message. 
    
    """
    ba = bitarray.bitarray()
    ba.fromstring(message)
    message_bit = ba.to01()
    length = len(message_bit)
    
    if length > 2**16:
        raise LongMessageException()
    
    binary_length = bin(length)[2:]
    length_bit = '0'*(16-len(binary_length))+ binary_length
    return length_bit+message_bit

def from_bits(encrypted_message):
    """
        This function returns the message from the sequence bits.
        
        The first 16 bits are analyzed to find the length of the message 
        to decode
    
    """    
    length = int(encrypted_message[:16],2)
    ba = bitarray.bitarray(encrypted_message[16:16+length])
    return ba.tostring()


def sub(num,bit):
    """
        This function returns the modified blue image component given the
        bit that needs to be encrypted.
        
        For instance if the actual blue component is 233:
            - if 1 needs to be encrypted, no modification is needed, because
            the least significant bit of the binary represenation of 233 is
            already 1
            - if 0 needs to be encrypted, the function returns 234
    
    """    
    if (bit == 0 and num%2 == 0) or (bit == 1 and num%2 != 0):
        return num
    else:
        return (num+1)%256

if __name__=='__main__':
    
    description = """ This program encrypts and decrypts a message inside an
    image using steganography.
    
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
    
    """
        
    try:    
        parser = argparse.ArgumentParser(description=description,
                                         formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('image',  help='input image')
        parser.add_argument('mode',  help='functioning mode', choices=['encrypt','decrypt'])
        parser.add_argument('-m','--message',  help='message to be encrypted')
        
        args = parser.parse_args()
        
        image_path = args.image
        mode = args.mode
        message = args.message

        if (mode == 'encrypt' and message == None):
            raise NoMessageException()
        if (mode == 'decrypt' and message != None):
            print "The given message will not be considered for the decryption"          
            
        image = Image.open(image_path)
        image_format = image.format

        if (mode == 'encrypt'):
            encrypt(image,message)
            image.save('encrypted_'+image_path,image_format)
        else:
            print decrypt(image)
        
    except IOError as e:
        print e
    except LongMessageException as e:
        print "The message is too long to be encrypted. See help"
    except SmallImageException as e:
        print "The image is too small to contain the message. See help"
    except NoMessageException as e:
        print "A message must be provided in encrypt mode"        
