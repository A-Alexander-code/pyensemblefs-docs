Installation
============

Requirements
------------

- Python 3.9 or higher
- A virtual environment is recommended (``venv`` or ``conda``)

From source
-----------

.. code-block:: bash

   git clone https://github.com/USER/pyensemblefs.git
   cd pyensemblefs
   python -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install -e .

Optional dependencies
---------------------

For visualization and extended functionality:

.. code-block:: bash

   pip install matplotlib seaborn upsetplot scikit-learn joblib pandas
