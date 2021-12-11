
import re
from pdf2image import convert_from_path
import pytesseract
from pytesseract import Output
from PIL import Image, ImageEnhance, ImageFilter
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'


def fetch_ocr(file_obj):
    images = convert_from_path(file_obj,
                               500, poppler_path=r'C:\Users\Triveni\Desktop\sai_project\poppler-0.68.0\bin')
    data = dict()
    for i, image in enumerate(images):
        img_index = 'page_'+str(i)
        data[img_index] = dict()
        # fname = 'C:/Users/Triveni/Desktop/sai_project/image'+str(i)+'.png'
        # image.save(fname, "PNG")

        im = image.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(im)
        im = enhancer.enhance(2)
        im = im.convert('1')
        # im.save('C:/Users/Triveni/Desktop/sai_project/temp2.jpg')

        text = pytesseract.image_to_string(im, config='--oem 3 --psm 6')
        # print(text)
        # print('-------------------------------------------------------')
        dct = pytesseract.image_to_data(im, output_type=Output.DICT)
        keys = list(dct.keys())
        n_boxes = len(dct['text'])

        for i in range(n_boxes):
            if 'VERIFICATION OF COVERAGE' in text:
                data[img_index]['type'] = 'VERIFICATION OF COVERAGE'
                if 'policy' in dct['text'][i].lower() and 'number' in dct['text'][i+1].lower() and (dct['text'][i+2]).isnumeric():
                    data[img_index]['policy_number'] = dct['text'][i+2]
                # date format
                if 'effective' in dct['text'][i].lower() and 'date' in dct['text'][i+1].lower():
                    data[img_index]['effective_date'] = dct['text'][i+2]
                if 'expiration' in dct['text'][i].lower() and 'date' in dct['text'][i+1].lower() and 'expiration_date' not in data[img_index]:
                    data[img_index]['expiration_date'] = dct['text'][i+2]
                if 'registered' in dct['text'][i].lower() and 'state' in dct['text'][i+1].lower() and 'registred_state' not in data[img_index]:
                    data[img_index]['registred_state'] = dct['text'][i+2]
                if 'vehicle' in dct['text'][i].lower() and 'year' in dct['text'][i+1].lower() and 'vehicle_year' not in data[img_index]:
                    data[img_index]['vehicle_year'] = dct['text'][i+2]
                if 'make' in dct['text'][i].lower() and 'make' not in data[img_index]:
                    data[img_index]['make'] = dct['text'][i+1]
                if 'model' in dct['text'][i].lower() and 'model' not in data[img_index]:
                    data[img_index]['model'] = dct['text'][i+1] + \
                        ' '+dct['text'][i+2]
                if 'vin' in dct['text'][i].lower() and 'vin' not in data[img_index]:
                    data[img_index]['vin'] = dct['text'][i+1] + dct['text'][i+2]
                # print(dct['text'][i], 'left', dct['left'][i], 'top', dct['top']
                    #   [i], 'width', dct['width'][i], 'height', dct['height'][i])
                if 'mailing' in dct['text'][i].lower() and 'address' in dct['text'][i+1].lower():
                    for j in range(n_boxes):
                        if dct['left'][i]-4 <= dct['left'][j] <= dct['left'][i]+2250 and dct['top'][i]+4 <= dct['top'][j] <= dct['top'][i]+370:
                            if 'mailing_address' in data[img_index].keys():
                                if dct['text'][j]:
                                    data[img_index]['mailing_address'] += ' ' + \
                                        " ".join(dct['text'][j].split())
                            else:
                                data[img_index]['mailing_address'] = " ".join(
                                    dct['text'][j].split())
                if 'mailing_address' in data[img_index].keys():
                    data[img_index]['mailing_address'] = data[img_index]['mailing_address'].strip(
                    )

            elif 'insurance Identification Card' in text:
                data[img_index]['type'] = 'Insurance Identification Card'
                if 'policy' in dct['text'][i].lower() and 'number' in dct['text'][i+1].lower():
                    for j in range(n_boxes):
                        if dct['left'][i]-4 <= dct['left'][j] <= dct['left'][i]+100 and dct['top'][i]+60 <= dct['top'][j] <= dct['top'][i]+65:
                            data[img_index]['policy_number'] = dct['text'][j]
                if 'effective' in dct['text'][i].lower() and 'date' in dct['text'][i+1].lower():
                    for j in range(n_boxes):
                        if dct['left'][i]-4 <= dct['left'][j] <= dct['left'][i]+100 and dct['top'][i] <= dct['top'][j] <= dct['top'][i]+65:
                            data[img_index]['effective_date'] = dct['text'][j][0:8]
                if 'expiration' in dct['text'][i].lower() and 'date' in dct['text'][i+1].lower():
                    for j in range(n_boxes):
                        if dct['left'][i]-4 <= dct['left'][j] <= dct['left'][i]+100 and dct['top'][i] <= dct['top'][j] <= dct['top'][i]+65:
                            data[img_index]['expiration_date'] = dct['text'][j][0:8]
                # print(dct['text'][i])
                if 'year' in dct['text'][i].lower():
                    for j in range(n_boxes):
                        if data[img_index].keys() and dct['left'][i]-4 <= dct['left'][j] <= dct['left'][i]+100 and dct['top'][i] <= dct['top'][j] <= dct['top'][i]+65:
                            try:
                                data[img_index]['year'] = int(dct['text'][j])
                            except:
                                pass
                if 'make' in dct['text'][i].lower():
                    for j in range(n_boxes):
                        if dct['left'][i]-20 <= dct['left'][j] <= dct['left'][i]+100 and dct['top'][i] <= dct['top'][j] <= dct['top'][i]+67 and 'make' not in dct['text'][j].lower():
                            data[img_index]['make'] = dct['text'][j]

                # ipdb.set_trace()
            else:
                data[img_index]['type'] = 'not supported document'
        return data

        # if dct['left'][i] <= 3000 and dct['top'][i] == 699:
        # print(dct['text'][i], 'left', dct['left'][i], 'top', dct['top']
        #   [i], 'width', dct['width'][i], 'height', dct['height'][i])
        # import ipdb
        # ipdb.set_trace()
