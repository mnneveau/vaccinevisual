#!/usr/bin/env python
import sys
import turtle
from random import randint

def getRandomColor():
    r = randint(0,255)
    g = randint(0,255)
    b = randint(0,255)
    return r, g, b

[script, input_file] = sys.argv

pep_seqs = []
with open(input_file, 'r') as input_f:
    header = input_f.readline().strip()
    for line in input_f:
        pep_seqs.append(line.strip())
#remove >, get peptide names and junction scores from FASTA input
edited_header = header[1:]
fields = edited_header.split("|")
pep_ids = fields[0].split(",")
junct_scores = fields[3].split(":")
junct_scores = junct_scores[1].split(",")

print(junct_scores)
print(pep_ids)

#find length of peptide sequences, use to determine proportion of each seqment
pep_len, total_len = [], 0
for pep in pep_seqs:
    pep_len.append(len(pep))
    total_len += len(pep)
#    conversion_factor = total_len / 360
    conversion_factor = 330 / total_len
print(pep_len)

#draw vaccine
t = turtle.Turtle()
myWin = turtle.Screen()
turtle.colormode(255)
t.speed(0)
t.hideturtle()
#t.circle(-50, 45)
t.pensize(5)
#white space in circle before genes
t.pencolor("white")
t.circle(-150,15)
inc = 0
for pep in pep_seqs:
    reset = t.pos()
    t.goto(t.pos() + (10,10 + inc))
    t.goto(reset)
    t.pencolor(getRandomColor())
    t.circle(-150, conversion_factor*len(pep))
    inc += - 5
#white space in circle after genes
t.pencolor("white")
t.circle(-150,15)
turtle.mainloop()
