#!/usr/bin/env python
import sys, os
import turtle

def output_screen():
    ps_file = "vaccine.ps"
    pdf_file = "vaccine.pdf"
    ts = t.getscreen()
    ts.getcanvas().postscript(file=ps_file)
    os.system('convert -density 100 -quality 100 ' + ps_file + " " + pdf_file)

#select color from scheme
def get_color(count):
    #option 1: 3 blue/green color scheme
    #scheme = [(161,218,180),(65,182,196),(44,127,184),(37,52,148)]
    #option 2: 11 color scheme
    scheme = [(166,206,227),(31,120,180),(178,223,138),(51,160,44),(251,154,153),(227,26,28),(253,191,111),(255,127,0),(202,178,214),(106,61,154),(177,89,40)]
    count =  count % len(scheme)
    return scheme[count]

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

#draw second line of junctions with amino acid additions
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

#draw arc for peptide
def draw_arc_peptide(peptide, length, count, angle):
    t.pencolor(get_color(count))
    t.circle(-200, (conversion_factor * length) / 2)
    t.pu()
    reset = t.heading()
    t.left(90)
    t.forward(65)
    if (angle > 80 and angle < 100) or (angle > 260 and angle < 280):
        t.write(peptide, align="center", font=("Arial", 9, "bold"))
    elif (angle > 0 and angle < 90) or (angle > 270 and angle < 360):
        t.write(peptide, align="right", font=("Arial", 9, "bold"))
    else:
        t.write(peptide, align="left", font=("Arial", 9, "bold"))
    t.back(65)
    t.setheading(reset)
    t.pd()
    t.circle(-200, (conversion_factor * length) / 2)

#draw arc for amino acid inserts to junctions
def draw_arc_junct(peptide, length):
    #t.pencolor("black")
    t.circle(-200, (conversion_factor * length) / 2)
    t.pu()
    reset = t.heading()
    t.left(90)
    t.back(25)
    t.write(peptide, align="center")
    t.forward(25)
    t.setheading(reset)
    t.pd()
    t.circle(-200, (conversion_factor * length) / 2)


[script, input_file] = sys.argv

pep_seqs = []
with open(input_file, 'r') as input_f:
    header = input_f.readline().strip()
    for line in input_f:
        pep_seqs.append(line.strip())
#remove >, get peptide names and junction scores from FASTA input
edited_header = header[1:]
fields = edited_header.split("|")
pep_ids_joined = fields[0].split(",")
pep_ids = []
for pep_id in pep_ids_joined:
    if "." in pep_id:
        mt, gene, var = pep_id.split(".")
        pep_id = "-".join((gene,var))
    pep_ids.append(pep_id)
junct_scores = fields[3].split(":")
junct_scores = junct_scores[1].split(",")

pep_dict = {}
for i in range(len(pep_ids)):
    pep_dict[pep_ids[i]] = pep_seqs[i]

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
t.setpos(-200,300)
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
t.circle(-200,15)
angle_parsed += 15
draw_junction()

junctions_parsed = 0
peptides_parsed = 0
for pep in pep_seqs:
    pep_length = len(pep)
    peptide = pep_ids[peptides_parsed]
    t.pensize(5)
    angle_parsed += conversion_factor * pep_length
    if pep_length > 8 and pep_length < 100:
        draw_arc_peptide(peptide, pep_length, junctions_parsed, angle_parsed)
        if junctions_parsed < len(junct_scores):
            draw_junction_w_label(junct_scores[junctions_parsed])
            junctions_parsed += 1
    elif pep_length < 8:
        draw_arc_junct(peptide, pep_length)
        draw_junction()
    else:
        print("Error: Peptide sequence over 100 amino acids inputted")
        sys.exit()
    peptides_parsed += 1

#add white space in circle after genes    
draw_junction()
t.pencolor("white")
t.circle(-200,15)
output_screen()

turtle.mainloop()


