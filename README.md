# assignment-python

###Requirements
* Python 3.5
* Chrome

###Installation and running the tests

* First, you need Homebrew on your system. You can simply run the following command to install it:

`/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

* Run this once you’re done to ensure Homebrew is installed and working properly:

`brew doctor`

* Now you can install Python 3.5 like this:

`brew install python3`

* If pip is not installed, you can install it using:

`sudo easy_install pip`

* If you prefer pip, then use the following command:

`sudo pip install selenium`

* Install behave:

`sudo pip install behave`

###Running the tests:

* Clone the repo:

`git clone https://github.com/Ivan-Cristian/assignment-python.git`

* From within the base directory, run behave:

`behave`

** You can run the test based on the feature file or tag:

`behave features/cart.feature`
Or
`behave -t cart`
