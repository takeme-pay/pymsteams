import setuptools

with open('README.md') as readme_file:
    README = readme_file.read()

setuptools.setup(
    name='takeme_pymsteams',
    version='1.0.0',
    description='Python Wrapper for pymsteams',
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=[
        'pymsteams',
        'shareplum'
    ],
    keywords='pymsteams MS Teams TakeMe',
    url='https://github.com/takeme-pay/pymsteams',
    author='Yukitaka Maeda',
    author_email='yukitaka.maeda@takeme.com',
    license='GPLv3+',
    packages=setuptools.find_packages(),
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ]
)
