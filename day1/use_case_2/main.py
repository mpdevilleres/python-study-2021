import os
import sys
import glob
from collections import OrderedDict

import click
from PyPDF2 import PdfFileMerger
from PyPDF2.pdf import PdfFileWriter, PdfFileReader
import shutil

VERSION = 1.00
BASEDIR = os.path.abspath(os.path.dirname(__file__))


class PdfTool(object):
    def __init__(self, base_dir, version):
        self.base_dir = base_dir
        self.input_dir = None
        self.output_dir = None
        self.dir_name = None

        self.version = version
        self.methods = OrderedDict(
            {'s': 'split',
             'm': 'merge',
             'r90': 'rotate_90',
             'r180': 'rotate_180',
             'r270': 'rotate_270',
             'c1': 'cut_1',
             'c2': 'cut_2',
             'q': 'quit'}
        )

    def split(self, input_pdf):
        if len(input_pdf) != 1:
            click.echo('Split requires and allows only 1 file at a time')
            return False

        with open(input_pdf.pop(), "rb") as f:
            in_pdf = PdfFileReader(f)
            for i in range(in_pdf.numPages):
                page_number = i + 1
                output = PdfFileWriter()
                output.addPage(in_pdf.getPage(i))
                output_file_page = os.path.join(self.output_dir, "page-{0:03d}.pdf".format(page_number))
                output_file = open(output_file_page, "wb")
                output.write(output_file)
                output_file.close()
        return True

    def merge(self, input_pdf):
        if len(input_pdf) <= 1:
            click.echo('Merge requires and allows 2 or more file at a time')
            return False

        merger = PdfFileMerger()

        for in_pdf in sorted(input_pdf):
            with open(in_pdf, "rb") as f:
                merger.append(PdfFileReader(f))

        output_file = os.path.join(self.output_dir, 'merged.pdf')
        merger.write(output_file)
        merger.close()

        return True

    def _rotate(self, input_pdf, angle):
        if len(input_pdf) != 1:
            click.echo('Rotate requires and allows only 1 file at a time')
            return False

        output = PdfFileWriter()

        with open(input_pdf.pop(), "rb") as f:
            in_pdf = PdfFileReader(f)

            for i in range(in_pdf.numPages):
                page = in_pdf.getPage(i)
                page.rotateClockwise(angle)

                output.addPage(page)

            output_filename = os.path.join(self.output_dir, 'rotated.pdf')
            output_file = open(output_filename, 'wb')
            output.write(output_file)
            output_file.close()
        return True

    def _cut(self, input_pdf, portion):
        if len(input_pdf) != 1:
            click.echo('Cut requires and allows only 1 file at a time')
            return False

        output = PdfFileWriter()
        with open(input_pdf.pop(), "rb") as f:
            in_pdf = PdfFileReader(f)
            for i in range(in_pdf.numPages):
                page = in_pdf.getPage(i)
                height = page.mediaBox.getUpperRight_y()
                width = page.mediaBox.getUpperRight_x()
                if portion == 1:
                    page.cropBox.lowerLeft = (0, 0)
                    page.cropBox.upperRight = (width, height / 2)
                elif portion == 2:
                    page.cropBox.lowerLeft = (0, height / 2)
                    page.cropBox.upperRight = (width, height)

                output.addPage(page)

            output_filename = os.path.join(self.output_dir, 'cut.pdf')
            output_file = open(output_filename, 'wb')
            output.write(output_file)
            output_file.close()

    @staticmethod
    def quit():
        sys.exit(0)

    def rotate_90(self, input_pdf):
        self._rotate(input_pdf, 90)

    def rotate_180(self, input_pdf):
        self._rotate(input_pdf, 180)

    def rotate_270(self, input_pdf):
        self._rotate(input_pdf, 270)

    def cut_1(self, input_pdf):
        self._cut(input_pdf, 1)

    def cut_2(self, input_pdf):
        self._cut(input_pdf, 2)

    def get_pdf(self):
        return [i for i in glob.iglob(self.input_dir + '/*.pdf')]

    def check_dir(self):
        self.input_dir = os.path.join(self.base_dir, 'to_' + self.dir_name)
        self.output_dir = os.path.join(self.base_dir, 'output_' + self.dir_name)

        # Checks of pdf exist in the output folder
        if os.path.isdir(self.output_dir) and os.listdir(self.output_dir):
            click.echo("deleting 'output_" + self.dir_name + "' files")
            shutil.rmtree(self.output_dir)
            click.echo("done deleting")
        elif not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir)

        if not os.path.isdir(self.input_dir):
            os.makedirs(self.input_dir)
            click.echo("\nPlease put your pdf inside 'to_" + self.dir_name + "' folder\n")

    @staticmethod
    def welcome_note():
        click.echo(
            "============================================\n" +
            "#------------------------------------------#\n" +
            "#                                          #\n" +
            "# PDF tool Using Python                    #\n" +
            "# Split, Merge, Rotate and Cut PDF Pages   #\n" +
            "#                                          #\n" +
            "#------------------------------------------#\n" +
            "============================================\n\n"
        )

    @staticmethod
    def show_help():
        click.echo(
            "s      - Split a pdf to separate pages\n" +
            "m      - Merge separate pages to single pdf file\n" +
            "r90    - Rotate Page 90 Degrees clockwise\n" +
            "r180   - Rotate Page 180 Degrees clockwise\n" +
            "r270   - Rotate Page 270 Degrees clockwise\n" +
            "c1     - Cut pdf and take lower part\n" +
            "c2     - Cut pdf and take upper part\n" +
            "q      - Quit Program\n"
        )

    def run(self):
        self.welcome_note()
        click.echo('Please Select your needs:')
        self.show_help()

        allowed_choices = self.methods.keys()

        choice = click.prompt('Please enter your choice ({})'.format(', '.join(allowed_choices)))
        while choice.lower() not in allowed_choices:
            choice = click.prompt('Please enter your choice ({})'.format(', '.join(allowed_choices)))

        self.dir_name = method = self.methods[choice]

        self.check_dir()
        input_pdf = self.get_pdf()

        success = getattr(self, method)(input_pdf)

        if success:
            click.echo("PDF " + method.capitalize() + " Finished, Please See the '" + self.output_dir + "' folder")


if __name__ == '__main__':
    tool = PdfTool(BASEDIR, VERSION)
    tool.run()
