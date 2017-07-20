#!/usr/bin/env python
import sys, os
import turtle
from random import randint

def output_screen():
    ps_file = "vaccine.ps"
    pdf_file = "vaccine.pdf"
    ts = t.getscreen()
    ts.getcanvas().postscript(file=ps_file)
    os.system('convert -density 100 -quality 100 ' + ps_file + " " + pdf_file)

#get random color code
def get_random_color():
    r = randint(0,255)
    g = randint(0,255)
    b = randint(0,255)
    return r, g, b

#draw perpindicular line to arc to mark junction
def draw_junction_w_label(junct_score):
    reset = t.heading()
    t.rt(90)
    t.pencolor("black")
    t.pensize(2)
    t.forward(10)
    t.back(20)
    t.pu()
    t.back(22)
    t.write(junct_score, align="center")
    t.forward(22)
    t.pd()
    t.forward(10)
    t.setheading(reset)
    return()

def draw_junction():
    reset = t.heading()
    t.rt(90)
    t.pencolor("black")
    t.pensize(2)
    t.forward(10)
    t.back(20)
    t.forward(10)
    t.setheading(reset)
    return()

def draw_arc_w_label_f(peptide, length):
    t.circle(-150, (conversion_factor * length) / 2)
    t.pu()
    reset = t.heading()
    t.left(90)
    t.forward(60)
    t.write(peptide, align="center")
    t.back(60)
    t.setheading(reset)
    t.pd()
    t.circle(-150, (conversion_factor * length) / 2)

def draw_arc_w_label_b(peptide, length):
    t.pencolor("black")
    t.circle(-150, (conversion_factor * length) / 2)
    t.pu()
    reset = t.heading()
    t.left(90)
    t.back(25)
    t.write(peptide, align="center")
    t.forward(25)
    t.setheading(reset)
    t.pd()
    t.circle(-150, (conversion_factor * length) / 2)


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



pep_dict = {}
for i in range(len(pep_ids)):
    pep_dict[pep_ids[i]] = pep_seqs[i]
print(pep_dict)

#determine what proportion of circle each peptide should take up
total_len = 0
for pep in pep_seqs:
    total_len += len(pep)   
    #30 degrees reserved for white space
    conversion_factor = 330 / total_len

#draw vaccine
t = turtle.Turtle()
myWin = turtle.Screen()
turtle.colormode(255)
#sets turtle orientation
turtle.mode("logo")
t.speed(0)
t.hideturtle()
t.pu()
t.setpos(-200,200)
t.write("Vaccine Design", font=("Arial", 18, "bold"))
t.pd()
t.pu()
t.setpos(-150,0)
t.pd()
t.pensize(5)
angle_parsed = 0
#white space in circle before genes
t.pencolor("white")
#negative radius draws circle clockwise
t.circle(-150,15)
angle_parsed += 15
draw_junction()

junctions_parsed = 0
peptides_parsed = 0
for pep in pep_seqs:
    pep_length = len(pep)
    peptide = pep_ids[peptides_parsed]
    t.pensize(5)
    t.pencolor(get_random_color())
    #draw 1st half of circle
    #if peptides_parsed
    #draw_arc_w_label_f(peptide, pep_length)
    #draw_arc_w_label_b(peptide, pep_length)
    #t.circle(-150, (conversion_factor * pep_length) / 2)
    #t.pu()
    #reset = t.heading()
    #t.left(90)
    #t.forward(95)
    #t.write(peptide, align="center")
    #t.back(95)
    #t.setheading(reset)
    #t.pd()
    #t.circle(-150, (conversion_factor * pep_length) / 2)
    angle_parsed += conversion_factor * pep_length
    if pep_length == 25:
        draw_arc_w_label_f(peptide, pep_length)
        if junctions_parsed < len(junct_scores):
            draw_junction_w_label(junct_scores[junctions_parsed])
            junctions_parsed += 1
    else:
        draw_arc_w_label_b(peptide, pep_length)
        draw_junction()
    peptides_parsed += 1
    

draw_junction()
#white space in circle after genes
t.pencolor("white")
t.circle(-150,15)

output_screen()

turtle.mainloop()


