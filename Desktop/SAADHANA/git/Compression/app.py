#!/usr/bin/env python3
from flask import Flask, render_template, request
from wtforms import Form, StringField
import huffman.compressor
import lzw.compressor
import shannon.compressor
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/success/<opfile>/<bsize>/<asize>')
def success(opfile, bsize, asize):
    return render_template('success.html', opfile = opfile, bsize = bsize, asize = asize)

class Submit(Form):
    source = StringField('Source')
    destination = StringField('Destination')
    cdc = StringField('Action (compress / decompress)')
    algorithm = StringField('Algorithm (huffman / lzw / shannon)')

@app.route('/submitform',methods=['GET','POST'])
def submitform():
    form = Submit(request.form)
    opfile = ""
    if request.method == 'POST':
        source = form.source.data
        destination = form.destination.data
        cdc = form.cdc.data
        algorithm = form.algorithm.data
        if cdc == "compress":
            opfile = compress(algorithm, source, destination)
            bsize = str(os.stat(source).st_size)
            asize = str(os.stat(opfile).st_size)
            return render_template('success.html', opfile = str(opfile), bsize = str(bsize), asize = str(asize))
        elif cdc == "decompress":
            opfile = decompress(algorithm, source, destination)
            bsize = str(os.stat(source).st_size)
            asize = str(os.stat(opfile).st_size)
            return render_template('success.html', opfile = str(opfile), bsize = str(bsize), asize = str(asize))
    return render_template('submitform.html', form=form)

def compress(alg, ipfile, opath):
    output_file = ''
    if alg == 'huffman':
        output_file = huffman.compressor.compress(ipfile, opath)
    elif alg == 'lzw':
        output_file = lzw.compressor.compress(ipfile, opath)
    else:
        output_file = shannon.compressor.compress(ipfile, opath)
    return output_file

def decompress(alg, ipfile, opath):
    output_file = ''
    if alg == 'lzw':
        output_file = lzw.decompressor.decompress(ipfile, opath)
    elif alg == 'huffman':
        output_file = huffman.decompressor.decompress(ipfile, opath)
    else:
        output_file = shannon.decompressor.decompress(ipfile, opath)
    return output_file

if __name__ == '__main__':
    app.run(debug=True, port=80)