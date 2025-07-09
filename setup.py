from setuptools import setup

setup(
    name='auxgen',
    version='0.0.2',    
    description='Auxiliary functions for Generative design',
    url='https://github.com/juancc/auxgen',
    author='Juan Carlos Arbelaez',
    author_email='jarbel16@eafit.edu.co',
    license= '',
    packages=['auxgen'],
    install_requires=[
                      'tqdm',
                      'numpy',
                      'matplotlib',
                      'numpy-stl'                     
                      ],
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)