#!/usr/bin/env python
import sys, os
import turtle

os.environ["DISPLAY"] = ':0.0'

#determine what proportion of circle each peptide should take up
def get_conversion_factor(pep_seqs):
    total_len = 0
    for pep in pep_seqs:
        total_len += len(pep)   
    #30 degrees reserved for white space
    conversion_factor = 330 / total_len
    return(conversion_factor)

def draw_header(t, header_pos):
    t.pu()
    t.setpos(header_pos)
    t.write("Vaccine Design", align="center", font=("Arial", 18, "bold"))
    t.pd()
    return()

def draw_wht_space(t, circle_radius, wht_space_angle):
    t.pencolor("white")
    t.circle(circle_radius,wht_space_angle)
    return()

#select color from scheme
def get_color(count):
    #option 1: 3 blue/green color scheme
    #scheme = [(161,218,180),(65,182,196),(44,127,184),(37,52,148)]
    #option 2: 6 color scheme
    scheme = [(31,120,180),(51,160,44),(227,26,28),(255,127,0),(106,61,154),(177,89,40)]
    count =  count % len(scheme)
    return scheme[count]

#draw perpindicular line to arc to mark junction
def draw_junction_w_label(junct_score, t, pen_thin, junct_score_space, angle):
    reset = t.heading()
    t.rt(90)
    t.pencolor("black")
    t.pensize(pen_thin)
    t.forward(10)
    t.back(20)
    t.pu()
    #t.back(junct_score_space)
    if (angle >= 0 and angle < 70):
        t.back(15)
        t.write(junct_score + 'nM', align="center")
        t.forward(15)
    elif (angle >= 65 and angle < 115):
        t.back(10)
        t.write(junct_score + 'nM', align="center")
        t.forward(10)
    elif (angle >= 115 and angle < 165):
        t.back(20)
        t.write(junct_score + 'nM', align="center")
        t.forward(20)
    elif (angle >= 165 and angle < 195):
        t.back(25)
        t.write(junct_score + 'nM', align="center")
        t.forward(25)
    elif (angle >= 195 and angle < 245):
        t.back(35)
        t.write(junct_score + 'nM', align="center")
        t.forward(35)
    elif (angle >= 245 and angle < 295):
        t.back(15)
        t.write(junct_score + 'nM', align="center")
        t.forward(15)
    else:
        t.back(20)
        t.write(junct_score + 'nM', align="center")
        t.forward(20)
    #t.write(junct_score + "nM", align="center")
    #t.forward(junct_score_space)
    t.pd()
    t.forward(10)
    t.setheading(reset)
    return()

#draw second line of junctions with amino acid additions
def draw_junction(t, pen_thin):
    reset = t.heading()
    t.rt(90)
    t.pencolor("black")
    t.pensize(pen_thin)
    t.forward(10)
    t.back(20)
    t.forward(10)
    t.setheading(reset)
    return()

#draw arc for peptide
def draw_arc_peptide(peptide, length, count, angle, t, circle_radius, conversion_factor, pep_id_space):
    t.pencolor(get_color(count))
    t.circle(circle_radius, (conversion_factor * length) / 2)
    t.pu()
    reset = t.heading()
    t.left(90)
    t.forward(pep_id_space)
    if (angle > 80 and angle < 100) or (angle > 260 and angle < 280):
        t.write(peptide, align="center", font=("Arial", 10, "bold"))
    elif (angle > 0 and angle < 90) or (angle > 270 and angle < 360):
        t.write(peptide, align="right", font=("Arial", 10, "bold"))
    else:
        t.write(peptide, align="left", font=("Arial", 10, "bold"))
    t.back(pep_id_space)
    t.setheading(reset)
    t.pd()
    t.circle(circle_radius, (conversion_factor * length) / 2)

#draw arc for amino acid inserts to junctions
def draw_arc_junct(peptide, length, t, conversion_factor, junct_seq_space, circle_radius):
    #t.pencolor("black")
    t.circle(circle_radius, (conversion_factor * length) / 2)
    t.pu()
    reset = t.heading()
    t.left(90)
    t.back(junct_seq_space)
    t.write(peptide, align="center")
    t.forward(junct_seq_space)
    t.setheading(reset)
    t.pd()
    t.circle(circle_radius, (conversion_factor * length) / 2)

#print turtle screen to a postscript file, convert to pdf
def output_screen(t):
    ps_file = "vaccine.ps"
    pdf_file = "vaccine.pdf"
    ts = t.getscreen()
    ts.getcanvas().postscript(file=ps_file)
    os.system('convert -density 100 -quality 200 ' + ps_file + " " + pdf_file)
    os.system('rm ' + ps_file)
    return()

def main(input_file=sys.argv[1]):
    min_pep_length = 8
    max_pep_length = 100

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

#Error if not a peptide sequence for every peptide ID
    if len(pep_ids) != len(pep_seqs):
        print("Error: Not an equal number of peptide sequences and peptide IDs")
        sys.exit()

    conversion_factor = get_conversion_factor(pep_seqs)

    #determine number of peptides (not including junction additions)
    num_peptides = 0
    for pep in pep_seqs:
        length = len(pep)
        if length > 8 and length < 25:
            num_peptides += 1

#draw vaccine
    t = turtle.Turtle()
    myWin = turtle.Screen()
    turtle.colormode(255)
    turtle.mode("logo")
    t.speed(0)
    t.hideturtle()

#negative radius draws circle clockwise
    circle_radius = -200
    circle_pos = (-200,0)
    header_pos = (0,0)
    wht_space_angle = 15
    pen_thick = 5
    pen_thin = 2
    pep_id_space = 45 + num_peptides 
    junct_seq_space = 25
    junct_score_space = 40

    draw_header(t, header_pos)
    t.pu()
    t.setpos(circle_pos)
    t.pd()
    t.pensize(pen_thick)
    angle_parsed = 0
#add white space in circle before genes
    draw_wht_space(t, circle_radius, wht_space_angle)
    angle_parsed += wht_space_angle
    draw_junction(t, pen_thin)

#draw main part of circle
    junctions_parsed = 0
    peptides_parsed = 0
    for pep in pep_seqs:
        pep_length = len(pep)
        peptide = pep_ids[peptides_parsed]
        t.pensize(pen_thick)
        angle_parsed += conversion_factor * pep_length
    #if length within reasonable range, draw and label arc for peptide
        if pep_length > min_pep_length and pep_length < max_pep_length:
            draw_arc_peptide(peptide, pep_length, junctions_parsed, angle_parsed, t, circle_radius, conversion_factor, pep_id_space)
            if junctions_parsed < len(junct_scores):
                draw_junction_w_label(junct_scores[junctions_parsed], t, pen_thin, junct_score_space, angle_parsed)
                junctions_parsed += 1
    #if length is less than minimum peptide length, assume amino acid addition to junction
        elif pep_length < min_pep_length:
                draw_arc_junct(peptide, pep_length, t, conversion_factor, junct_seq_space, circle_radius)
                draw_junction(t, pen_thin)
        else:
                print("Error: Peptide sequence over 100 amino acids inputted")
                sys.exit()
        peptides_parsed += 1

#add white space in circle after genes    
    draw_junction(t, pen_thin)
    draw_wht_space(t, circle_radius, wht_space_angle)
    output_screen(t)

    turtle.mainloop()

main()

