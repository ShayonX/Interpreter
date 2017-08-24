About the Solution:

In a statement there are several tokens. While developing the program I have resorted to a method of separating the tokens. After this separation I have used a lexical analyzer to utilize the tokens as per their attributes. I have used several classes, objects and several functions to make the interpreter modular. I have also implemented the concepts of inheritance and encapsulation to make the interpreter more efficient.

My interpreter can work on basic statements as mentioned in the defined language:

  statements  s ::=  x = e  |   print e  | s s
  expressions e ::=  x  |  n  |  e + e  |  e - e  |  e * e  | e / e
  variables   x
  integers    n
  
It can also cater to:
1. Integers with multiple digits.
2. Intermittent Spaces
3. variables and integers in any order or volume

It can be refined further but as mentioned in the exercise this is a bare bones interpreter with the requested functionality.

Documentation has been provided in the form of comprehensive COMMENTS throughout the code.

Assessment Exercise

Question:
How many types of tokens will you have to recognize and how will you implement it?

Answer:
Best Answer from a student who has mastered the concepts:

Will Mention-
-Variable, Integer, Assignment Operator, Arithmetic Operators,Space and Print.
-Will mention that variables will have an extra attribute as it will store values as well,hence lexical analysis has to take this into consideration.
-Will mention how to cater to multiple digit Integers.
-Will mention a way to deal with intermittent spaces.
-Excellent understanding will also prompt them to tell us that BODMAS rule has to be applied in arithmetic so the lexical analyzer can store expression in Post-Fix form in a data structure. 

Acceptable Answer:

-Variable, Integer, Assignment Operator, Arithmetic Operators,Space and Print.
-Will mention that variables will have an extra attribute as it will store values as well, hence during lexical analysis this has to be taken into consideration.
-Will mention a way to deal with intermittent spaces.
Insufficient Answer
-Will mention a few tokens but will not be able to analyse it from the perspective of a lexical analyzer.

Thank You.
