# -*- coding: utf-8 -*-

#
#    Orvet programming language interpreter.
#    Copyright (C) 2016  Renaud Sirdey (renaud.sirdey@gmail.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import random
import codecs
import time

version='0.1'
program=[]
int_vars=dict()
bool_vars=dict()
dict_vars=dict()
proc_table=dict()
trace=False
interactive=True
chrono=False

def load_program(prog_name):
    global program
    print('Chargement du programme')
    program = codecs.open(prog_name, 'r', encoding='utf-8').readlines()
    print(len(program),'lignes chargées')
        
def print_program():
    nb_digits = len(str(len(program)))
    form_str = '{{:{0}}} - {{}}'.format(nb_digits)
    l=0
    print('Programme :')
    for line in program:
        print(form_str.format(l,line),end='')
        l=l+1

def print_int_vars():
    print('Entiers :')
    for var,val in sorted(int_vars.items()):
        print(var,'=',val)

def int_to_char(v):
    if v>=0 and v<10:
        return chr(v+ord('0'))
    if v>=10 and v<36:
        return chr(v-10+ord('A'))
    if v>=36 and v<62:
        return chr(v-36+ord('a'))
    if v==62:
        return ' '
    if v==63:
        return '.'
    if v==64:
        return 'à'
    if v==65:
        return 'â'
    if v==66:
        return 'ç'
    if v==67:
        return 'é'
    if v==68:
        return 'è'
    if v==69:
        return 'ê'
    if v==70:
        return 'ë'
    if v==71:
        return 'î'
    if v==72:
        return 'ï'
    if v==73:
        return 'ô'
    if v==74:
        return 'ö'
    if v==75:
        return 'ù'
    return '?'

def char_to_int(c):
    if c>='0' and c<='9':
        return ord(c)-ord('0')
    if c>='A' and c<='Z':
        return ord(c)-ord('A')+10
    if c>='a' and c<='z':
        return ord(c)-ord('a')+36
    if c=='_' or c==' ':
        return 62
    if c=='.':
        return 63
    if c=='à':
        return 64
    if c=='â':
        return 65 
    if c=='ç':
        return 66
    if c=='é':
        return 67 
    if c=='è':
        return 68 
    if c=='ê':
        return 69 
    if c=='ë':
        return 70 
    if c=='î':
        return 71 
    if c=='ï':
        return 72 
    if c=='ô':
        return 73 
    if c=='ö':
        return 74 
    if c=='ù':
        return 75
    return -1
        
def bool_to_str(b):
    if b==True:
        return 'vrai'
    return 'faux'
    
def print_bool_vars():
    print('Booléens :')
    for var,val in sorted(bool_vars.items()):
        print(var,'=',bool_to_str(val))

def print_dict_vars():
    print('Dictionnaires :')
    for var,val in sorted(dict_vars.items()):
        print(var,'=',val)
    
def print_proc_table():
    print('Procédures :')
    for name,ip in sorted(proc_table.items()):
        print(name,'@',ip)
        
def print_memory():
    print('Mémoire :')
    print_int_vars()
    print_bool_vars()
    print_dict_vars()
    print_proc_table()

def check_label(token):
    if len(token)==0:
        return False
    if not token[0].isalpha():
        return False
    for i in range(1,len(token)):
       if not (token[i].isalnum() or token[i]=='_'):
            return False
    return True
    
def check_int(token):
    if len(token)==0:
        return False
    if token.isdecimal():
        return True
    if token[0]=='-':
        if token.split('-')[1].isdecimal():
            return True
    return False
    
def check_char(token):
    if len(token)!=1:
        return False
    if token>='0' and token<='9':
        return True
    if token>='A' and token<='Z':
        return True
    if token>='a' and token<='z':
        return True
    if token=='_':
        return True
    if token=='.':
        return True
    if token=='à':
        return True
    if token=='â':
        return True 
    if token=='ç':
        return True
    if token=='é':
        return True 
    if token=='è':
        return True 
    if token=='ê':
        return True 
    if token=='ë':
        return True 
    if token=='î':
        return True 
    if token=='ï':
        return True 
    if token=='ô':
        return True 
    if token=='ö':
        return True 
    if token=='ù':
        return True
    return False
        
def is_int_var(var):
    return var in int_vars

def is_bool_var(var):
    return var in bool_vars
    
def is_dict_var(var):
    return var in dict_vars
    
def is_proc(name):
    return name in proc_table

def is_defined(var):
    if is_int_var(var):
        return True
    if is_bool_var(var):
        return True
    if is_dict_var(var):
        return True
    return False

def is_proc_defined(name):
    if is_proc(name):
        return True

def line_num(ip):
    return ip+1
    
def assert_var_def(ip,token):
    if not check_label(token):
        print('Erreur ligne',line_num(ip),':',token,'n\'est pas un nom de variable valide')
        return False
    if not is_defined(token):
        print('Erreur ligne',line_num(ip),': la variable',token,'n\'est pas définie')
        return False
    return True

# This whole "skip" story is for handling conditionnal execution 
# while still parsing the instructions.    
def parse_int_instr(ip,tokens,skip):
    if tokens[0]=='entier':
        if len(tokens)!=2:
            print('Erreur ligne',line_num(ip),': syntaxe de déclaration incorrecte d\'un entier')
            return -1
        if not check_label(tokens[1]):
            print('Erreur ligne',line_num(ip),':',tokens[1],'n\'est pas un nom de variable valide')
            return -1
        if is_defined(tokens[1]):
            print('Erreur ligne',line_num(ip),': une variable',tokens[1],'est déjà définie')
            return -1
        if not skip:
            int_vars[tokens[1]]=0
            if trace:
                print(line_num(ip),'- Définition de l\'entier',tokens[1],'(initialisé à 0)')
        return ip+1
    else:
        return -1

def parse_bool_instr(ip,tokens,skip):
    if tokens[0]=='booléen':
        if len(tokens)!=2:
            print('Erreur ligne',line_num(ip),': syntaxe de déclaration incorrecte d\'un booléen')
            return -1
        if not check_label(tokens[1]):
            print('Erreur ligne',line_num(ip),':',tokens[1],'n\'est pas un nom de variable valide')
            return -1
        if is_defined(tokens[1]):
            print('Erreur ligne',line_num(ip),': une variable',tokens[1],'est déjà définie')
            return -1
        if not skip:
            bool_vars[tokens[1]]=False
            if trace:
                print(line_num(ip),'- Définition du booléen',tokens[1],'(initialisé à faux)')
        return ip+1
    else:
        return -1
        
def parse_read_instr(ip,tokens,skip):
    if tokens[0]=='lire':
        if len(tokens)!=2:
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de lecture incorrecte')
            return -1
        if not assert_var_def(ip,tokens[1]):
            return -1
        if not skip:
            if is_int_var(tokens[1]):
                val=input('Valeur de l\'entier '+tokens[1]+' ? ').strip()
                while not check_int(val) and not check_char(val):
                    print('\'',val,'\' n\'est ni un entier ni un caractère !')
                    val=input('Valeur de l\'entier '+tokens[1]+' ? ')
                if check_int(val):    
                    int_vars[tokens[1]]=int(val)
                if check_char(val):
                    int_vars[tokens[1]]=char_to_int(val)                    
                if trace:
                    print(line_num(ip),'- Lecture de la valeur de l\'entier',tokens[1])
        return ip+1
    else:
        return -1
        
def parse_show_instr(ip,tokens,skip):
    if tokens[0]=='montrer':
        if len(tokens)!=2:
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction d\'écriture incorrecte')
            return -1
        if not assert_var_def(ip,tokens[1]):
            return -1
        if not skip:
            if is_int_var(tokens[1]):
                print(tokens[1],'=',int_vars[tokens[1]])
                if trace:
                    print(line_num(ip),'- Ecriture de la valeur de l\'entier',tokens[1])
            if is_bool_var(tokens[1]):
                print(tokens[1],'=',bool_to_str(bool_vars[tokens[1]]))
                if trace:
                    print(line_num(ip),'- Ecriture de la valeur du booléen',tokens[1])                    
        return ip+1
    else:
        return -1

def check_int_value(token):
    if check_int(token):
        return True
    if check_label(token) and is_int_var(token):
        return True
    return False

# check_int_value must be called before!
def get_int_value(token):
    if check_int(token):
        return int(token)
    return int_vars[token]

def check_bool_value(token):
    if token=='vrai' or token=='faux':
        return True
    if check_label(token) and is_bool_var(token):
        return True
    return False

# check_bool_value must be called before!    
def get_bool_value(token):
    if token=='vrai':
        return True
    if token=='faux':
        return False
    return bool_vars[token]
    
def do_int_assign(ip,source,dest,skip):
    if not check_int_value(source):
        print('Erreur ligne',line_num(ip),':',source,'n\'est pas une source d\'affectation valide pour une variable entière')
        return -1
    if not skip:
        val=get_int_value(source)
        int_vars[dest]=val
        if trace:
            print(line_num(ip),'- Affectation de la valeur',val,'à la variable entière',dest)
    return ip+1

def do_bool_assign(ip,source,dest,skip):
    if not check_bool_value(source):
        print('Erreur ligne',line_num(ip),':',source,'n\'est pas une source d\'affectation valide pour une variable booléenne')
        return -1
    if not skip:
        val=get_bool_value(source)
        bool_vars[dest]=val
        if trace:
            print(line_num(ip),'- Affectation de la valeur',bool_to_str(val),'à la variable booléenne',dest)
    return ip+1
    
def parse_assign_instr(ip,tokens,skip):
    if tokens[0]=='affecter':
        if len(tokens)!=4 or (tokens[2]!='à' and tokens[2]!='dans'):
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction d\'affectation incorrecte')
            return -1
        if not assert_var_def(ip,tokens[3]):
            return -1
        if is_int_var(tokens[3]):
            return do_int_assign(ip,tokens[1],tokens[3],skip)
        if is_bool_var(tokens[3]):
            return do_bool_assign(ip,tokens[1],tokens[3],skip)
        print('Erreur ligne',line_num(ip),': type incorrect pour la variable d\'affectation')
        return -1
    else:
        return -1
       
def do_int_add(ip,source1,source2,dest,skip):
    if not check_int_value(source1):
        print('Erreur ligne',line_num(ip),':',source1,'n\'est pas une opérande valide pour une addition entière')
        return -1
    if not check_int_value(source2):
        print('Erreur ligne',line_num(ip),':',source2,'n\'est pas une opérande valide pour une addition entière')
        return -1
    if not skip:
        val1=get_int_value(source1)
        val2=get_int_value(source2)
        int_vars[dest]=val1+val2
        if trace:
            print(line_num(ip),'- Addition des valeurs',val1,'et',val2,'dans la variable entière',dest)
    return ip+1
    
def parse_add_instr(ip,tokens,skip):
    if tokens[0]=='ajouter':
        if len(tokens)!=6 or (tokens[2]!='à' and tokens[2]!='et' and tokens[2]!='avec') or tokens[4]!='dans':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction d\'addition incorrecte')
            return -1
        if not assert_var_def(ip,tokens[5]):
            return -1
        if is_int_var(tokens[5]):
            return do_int_add(ip,tokens[1],tokens[3],tokens[5],skip)
        print('Erreur ligne',line_num(ip),': type incorrect pour la variable d\'affectation')
        return -1
    else:
        return -1

def do_int_mul(ip,source1,source2,dest,skip):
    if not check_int_value(source1):
        print('Erreur ligne',line_num(ip),':',source1,'n\'est pas une opérande valide pour une multiplication entière')
        return -1
    if not check_int_value(source2):
        print('Erreur ligne',line_num(ip),':',source2,'n\'est pas une opérande valide pour une multiplication entière')
        return -1
    if not skip:
        val1=get_int_value(source1)
        val2=get_int_value(source2)
        int_vars[dest]=val1*val2
        if trace:
            print(line_num(ip),'- Multiplication des valeurs',val1,'et',val2,'dans la variable entière',dest)
    return ip+1
        
def parse_mul_instr(ip,tokens,skip):
    if tokens[0]=='multiplier':
        if len(tokens)!=6 or (tokens[2]!='par' and tokens[2]!='à' and tokens[2]!='et' and tokens[2]!='avec') or tokens[4]!='dans':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de multiplication incorrecte')
            return -1
        if not assert_var_def(ip,tokens[5]):
            return -1
        if is_int_var(tokens[5]):
            return do_int_mul(ip,tokens[1],tokens[3],tokens[5],skip)
        print('Erreur ligne',line_num(ip),': type incorrect pour la variable d\'affectation')
        return -1
    else:
        return -1

def do_int_sub(ip,source1,source2,dest,skip):
    if not check_int_value(source1):
        print('Erreur ligne',line_num(ip),':',source1,'n\'est pas une opérande valide pour une soustraction entière')
        return -1
    if not check_int_value(source2):
        print('Erreur ligne',line_num(ip),':',source2,'n\'est pas une opérande valide pour une soustraction entière')
        return -1
    if not skip:
        val1=get_int_value(source1)
        val2=get_int_value(source2)
        int_vars[dest]=val2-val1
        if trace:
            print(line_num(ip),'- Soustraction de la valeur',val1,'à la valeur',val2,'dans la variable entière',dest)
    return ip+1
                
def parse_sub_instr(ip,tokens,skip):
    if tokens[0]=='soustraire':
        if len(tokens)!=6 or tokens[2]!='à' or tokens[4]!='dans':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de soustraction incorrecte')
            return -1
        if not assert_var_def(ip,tokens[5]):
            return -1
        if is_int_var(tokens[5]):
            return do_int_sub(ip,tokens[1],tokens[3],tokens[5],skip)
        print('Erreur ligne',line_num(ip),': type incorrect pour la variable d\'affectation')
        return -1
    else:
        return -1

def do_int_div(ip,source1,source2,dest,skip):
    if not check_int_value(source1):
        print('Erreur ligne',line_num(ip),':',source1,'n\'est pas une opérande valide pour une division entière')
        return -1
    if not check_int_value(source2):
        print('Erreur ligne',line_num(ip),':',source2,'n\'est pas une opérande valide pour une division entière')
        return -1
    if not skip:
        val1=get_int_value(source1)
        val2=get_int_value(source2)
        if val2==0:
            print('Erreur ligne',line_num(ip),': division par zéro !')
            return -1
        int_vars[dest]=int(val1//val2) # // = floordiv operator.
        if trace:
            print(line_num(ip),'- Division de la valeur',val1,'par la valeur',val2,'dans la variable entière',dest)
    return ip+1
        
def parse_div_instr(ip,tokens,skip):
    if tokens[0]=='diviser':
        if len(tokens)!=6 or tokens[2]!='par' or tokens[4]!='dans':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de division incorrecte')
            return -1
        if not assert_var_def(ip,tokens[5]):
            return -1
        if is_int_var(tokens[5]):
            return do_int_div(ip,tokens[1],tokens[3],tokens[5],skip)
        print('Erreur ligne',line_num(ip),': type incorrect pour la variable d\'affectation')
        return -1
    else:
        return -1

def do_int_mod(ip,source1,source2,dest,skip):
    if not check_int_value(source1):
        print('Erreur ligne',line_num(ip),':',source1,'n\'est pas une opérande valide pour une réduction modulaire')
        return -1
    if not check_int_value(source2):
        print('Erreur ligne',line_num(ip),':',source2,'n\'est pas une opérande valide pour une réduction modulaire')
        return -1
    if not skip:
        val1=get_int_value(source1)
        val2=get_int_value(source2)
        if val2==0:
            print('Erreur ligne',line_num(ip),': division par zéro !')
            return -1
        int_vars[dest]=val1%val2
        if trace:
            print(line_num(ip),'- Réduction de la valeur',val1,'modulo la valeur',val2,'dans la variable entière',dest)
    return ip+1

def parse_mod_instr(ip,tokens,skip):
    if tokens[0]=='réduire':
        if len(tokens)!=6 or tokens[2]!='modulo' or tokens[4]!='dans':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de réduction modulaire incorrecte')
            return -1
        if not assert_var_def(ip,tokens[5]):
            return -1
        if is_int_var(tokens[5]):
            return do_int_mod(ip,tokens[1],tokens[3],tokens[5],skip)
        print('Erreur ligne',line_num(ip),': type incorrect pour la variable d\'affectation')
        return -1
    else:
        return -1

def do_int_pow(ip,source1,source2,dest,skip):
    if not check_int_value(source1):
        print('Erreur ligne',line_num(ip),':',source1,'n\'est pas une opérande valide pour une élévation à la puissance')
        return -1
    if not check_int_value(source2):
        print('Erreur ligne',line_num(ip),':',source2,'n\'est pas une opérande valide pour une élévation à la puissance')
        return -1
    if not skip:
        val1=get_int_value(source1)
        val2=get_int_value(source2)
        if val2<0:
            print('Erreur ligne',line_num(ip),': élévation à une puissance négative !')
            return -1
        int_vars[dest]=val1**val2
        if trace:
            print(line_num(ip),'- Elévation de la valeur',val1,'à la puissance',val2,'dans la variable entière',dest)
    return ip+1        
        
def parse_pow_instr(ip,tokens,skip):
    if tokens[0]=='élever':
        if len(tokens)!=8 or tokens[2]!='à' or tokens[3]!='la' or tokens[4]!='puissance' or tokens[6]!='dans':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction puissance incorrecte')
            return -1
        if not assert_var_def(ip,tokens[7]):
            return -1
        if is_int_var(tokens[7]):
            return do_int_pow(ip,tokens[1],tokens[5],tokens[7],skip)
        print('Erreur ligne',line_num(ip),': type incorrect pour la variable d\'affectation')
        return -1
    else:
        return -1
                
def do_int_max(ip,source1,source2,dest,skip):
    if not check_int_value(source1):
        print('Erreur ligne',line_num(ip),':',source1,'n\'est pas une opérande valide pour une maximisation')
        return -1
    if not check_int_value(source2):
        print('Erreur ligne',line_num(ip),':',source2,'n\'est pas une opérande valide pour une maximisation')
        return -1
    if not skip:
        val1=get_int_value(source1)
        val2=get_int_value(source2)
        int_vars[dest]=max(val1,val2)
        if trace:
            print(line_num(ip),'- Maximisation des valeurs',val1,'et',val2,'dans la variable entière',dest)
    return ip+1

def parse_max_instr(ip,tokens,skip):
    if tokens[0]=='maximiser':
        if len(tokens)!=6 or tokens[2]!='et' or tokens[4]!='dans':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de maximisation incorrecte')
            return -1
        if not assert_var_def(ip,tokens[5]):
            return -1
        if is_int_var(tokens[5]):
            return do_int_max(ip,tokens[1],tokens[3],tokens[5],skip)
        print('Erreur ligne',line_num(ip),': type incorrect pour la variable d\'affectation')
        return -1
    else:
        return -1

def do_int_min(ip,source1,source2,dest,skip):
    if not check_int_value(source1):
        print('Erreur ligne',line_num(ip),':',source1,'n\'est pas une opérande valide pour une minimisation')
        return -1
    if not check_int_value(source2):
        print('Erreur ligne',line_num(ip),':',source2,'n\'est pas une opérande valide pour une minimisation')
        return -1
    if not skip:
        val1=get_int_value(source1)
        val2=get_int_value(source2)
        int_vars[dest]=min(val1,val2)
        if trace:
            print(line_num(ip),'- Minimisation des valeurs',val1,'et',val2,'dans la variable entière',dest)
    return ip+1

def parse_min_instr(ip,tokens,skip):
    if tokens[0]=='minimiser':
        if len(tokens)!=6 or tokens[2]!='et' or tokens[4]!='dans':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de minimisation incorrecte')
            return -1
        if not assert_var_def(ip,tokens[5]):
            return -1
        if is_int_var(tokens[5]):
            return do_int_min(ip,tokens[1],tokens[3],tokens[5],skip)
        print('Erreur ligne',line_num(ip),': type incorrect pour la variable d\'affectation')
        return -1
    else:
        return -1

def do_int_cmp(ip,source1,source2,dest,skip):
    if not check_int_value(source1):
        print('Erreur ligne',line_num(ip),':',source1,'n\'est pas une opérande valide pour une comparaison d\'entiers')
        return -1
    if not check_int_value(source2):
        print('Erreur ligne',line_num(ip),':',source2,'n\'est pas une opérande valide pour une comparaison d\'entiers')
        return -1
    if not skip:
        val1=get_int_value(source1)
        val2=get_int_value(source2)
        bool_vars[dest]=val1==val2
        if trace:
            print(line_num(ip),'- Comparaison des valeurs',val1,'et',val2,'dans la variable booléenne',dest)
    return ip+1
        
def parse_cmp_instr(ip,tokens,skip):
    if tokens[0]=='comparer':
        if len(tokens)!=6 or (tokens[2]!='avec' and tokens[2]!='et' and tokens[2]!='à') or tokens[4]!='dans':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de comparaison incorrecte')
            return -1
        if not assert_var_def(ip,tokens[5]):
            return -1
        if is_bool_var(tokens[5]):
            return do_int_cmp(ip,tokens[1],tokens[3],tokens[5],skip)
        print('Erreur ligne',line_num(ip),': type incorrect pour la variable d\'affectation')
        return -1
    else:
        return -1

def do_int_neq(ip,source1,source2,dest,skip):
    if not check_int_value(source1):
        print('Erreur ligne',line_num(ip),':',source1,'n\'est pas une opérande valide pour un test de non égalité d\'entiers')
        return -1
    if not check_int_value(source2):
        print('Erreur ligne',line_num(ip),':',source2,'n\'est pas une opérande valide pour un test de non égalité d\'entiers')
        return -1
    if not skip:
        val1=get_int_value(source1)
        val2=get_int_value(source2)
        bool_vars[dest]=val1!=val2
        if trace:
            print(line_num(ip),'- Test de la non égalité des valeurs',val1,'et',val2,'dans la variable booléenne',dest)
    return ip+1

def parse_neq_instr(ip,tokens,skip):
    if tokens[0]=='différencier':
        if len(tokens)!=6 or (tokens[2]!='avec' and tokens[2]!='et' and tokens[2]!='à') or tokens[4]!='dans':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de différenciation incorrecte')
            return -1
        if not assert_var_def(ip,tokens[5]):
            return -1
        if is_bool_var(tokens[5]):
            return do_int_neq(ip,tokens[1],tokens[3],tokens[5],skip)
        print('Erreur ligne',line_num(ip),': type incorrect pour la variable d\'affectation')
        return -1
    else:
        return -1
                
def do_int_lower(ip,source1,source2,dest,skip):
    if not check_int_value(source1):
        print('Erreur ligne',line_num(ip),':',source1,'n\'est pas une opérande valide pour une minoration d\'entiers')
        return -1
    if not check_int_value(source2):
        print('Erreur ligne',line_num(ip),':',source2,'n\'est pas une opérande valide pour une minoration d\'entiers')
        return -1
    if not skip:
        val1=get_int_value(source1)
        val2=get_int_value(source2)
        bool_vars[dest]=val2<val1
        if trace:
            print(line_num(ip),'- Minoration de la valeur',val1,'par la valeur',val2,'dans la variable booléenne',dest)
    return ip+1

def parse_lower_instr(ip,tokens,skip):
    if tokens[0]=='minorer':
        if len(tokens)!=6 or tokens[2]!='par' or tokens[4]!='dans':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de minoration incorrecte')
            return -1
        if not assert_var_def(ip,tokens[5]):
            return -1
        if is_bool_var(tokens[5]):
            return do_int_lower(ip,tokens[1],tokens[3],tokens[5],skip)
        print('Erreur ligne',line_num(ip),': type incorrect pour la variable d\'affectation')
        return -1
    else:
        return -1

def do_int_upper(ip,source1,source2,dest,skip):
    if not check_int_value(source1):
        print('Erreur ligne',line_num(ip),':',source1,'n\'est pas une opérande valide pour une majoration d\'entiers')
        return -1
    if not check_int_value(source2):
        print('Erreur ligne',line_num(ip),':',source2,'n\'est pas une opérande valide pour une majoration d\'entiers')
        return -1
    if not skip:
        val1=get_int_value(source1)
        val2=get_int_value(source2)
        bool_vars[dest]=val2>val1
        if trace:
            print(line_num(ip),'- Majoration de la valeur',val1,'par la valeur',val2,'dans la variable booléenne',dest)
    return ip+1

def parse_upper_instr(ip,tokens,skip):
    if tokens[0]=='majorer':
        if len(tokens)!=6 or tokens[2]!='par' or tokens[4]!='dans':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de majoration incorrecte')
            return -1
        if not assert_var_def(ip,tokens[5]):
            return -1
        if is_bool_var(tokens[5]):
            return do_int_upper(ip,tokens[1],tokens[3],tokens[5],skip)
        print('Erreur ligne',line_num(ip),': type incorrect pour la variable d\'affectation')
        return -1
    else:
        return -1

def do_bool_disj(ip,source1,source2,dest,skip):
    if not check_bool_value(source1):
        print('Erreur ligne',line_num(ip),':',source1,'n\'est pas une opérande valide pour une disjonction booléenne')
        return -1
    if not check_bool_value(source2):
        print('Erreur ligne',line_num(ip),':',source2,'n\'est pas une opérande valide pour une disjonction booléenne')
        return -1
    if not skip:
        val1=get_bool_value(source1)
        val2=get_bool_value(source2)
        bool_vars[dest]=val2 or val1
        if trace:
            print(line_num(ip),'- Disjonction (OU logique) des valeurs booléennes',val1,'et',val2,'dans la variable booléenne',dest)
    return ip+1

def parse_disj_instr(ip,tokens,skip): # I.e., inclusive-OR
    if tokens[0]=='disjoindre':
        if len(tokens)!=6 or (tokens[2]!='et' and tokens[2]!='avec') or tokens[4]!='dans':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de disjonction (OU logique) incorrecte')
            return -1
        if not assert_var_def(ip,tokens[5]):
            return -1
        if is_bool_var(tokens[5]):
            return do_bool_disj(ip,tokens[1],tokens[3],tokens[5],skip)
        print('Erreur ligne',line_num(ip),': type incorrect pour la variable d\'affectation')
        return -1
    else:
        return -1

def do_bool_conj(ip,source1,source2,dest,skip):
    if not check_bool_value(source1):
        print('Erreur ligne',line_num(ip),':',source1,'n\'est pas une opérande valide pour une conjonction booléenne')
        return -1
    if not check_bool_value(source2):
        print('Erreur ligne',line_num(ip),':',source2,'n\'est pas une opérande valide pour une conjonction booléenne')
        return -1
    if not skip:
        val1=get_bool_value(source1)
        val2=get_bool_value(source2)
        bool_vars[dest]=val2 and val1
        if trace:
            print(line_num(ip),'- Conjonction (ET logique) des valeurs booléennes',val1,'et',val2,'dans la variable booléenne',dest)
    return ip+1

def parse_conj_instr(ip,tokens,skip): # I.e., AND
    if tokens[0]=='conjoindre':
        if len(tokens)!=6 or (tokens[2]!='et' and tokens[2]!='avec') or tokens[4]!='dans':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de conjonction (ET logique) incorrecte')
            return -1
        if not assert_var_def(ip,tokens[5]):
            return -1
        if is_bool_var(tokens[5]):
            return do_bool_conj(ip,tokens[1],tokens[3],tokens[5],skip)
        print('Erreur ligne',line_num(ip),': type incorrect pour la variable d\'affectation')
        return -1
    else:
        return -1

def do_bool_comp(ip,source,dest,skip):
    if not check_bool_value(source):
        print('Erreur ligne',line_num(ip),':',source1,'n\'est pas une opérande valide pour une complémentation booléenne')
        return -1
    if not skip:
        val=get_bool_value(source)
        bool_vars[dest]=not val
        if trace:
            print(line_num(ip),'- Complémentation (NON logique) de la valeur booléenne',val,'dans la variable booléenne',dest)
    return ip+1

def parse_comp_instr(ip,tokens,skip): # I.e., AND
    if tokens[0]=='complémenter':
        if len(tokens)!=4 or tokens[2]!='dans':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de complémentation (NON logique) incorrecte')
            return -1
        if not assert_var_def(ip,tokens[3]):
            return -1
        if is_bool_var(tokens[3]):
            return do_bool_comp(ip,tokens[1],tokens[3],skip)
        print('Erreur ligne',line_num(ip),': type incorrect pour la variable d\'affectation')
        return -1
    else:
        return -1

def do_int_random(ip,source1,source2,dest,skip):
    if not check_int_value(source1):
        print('Erreur ligne',line_num(ip),':',source1,'n\'est pas une opérande valide pour un tirage aléatoire')
        return -1
    if not check_int_value(source2):
        print('Erreur ligne',line_num(ip),':',source2,'n\'est pas une opérande valide pour un tirage aléatoire')
        return -1
    if not skip:
        val1=get_int_value(source1)
        val2=get_int_value(source2)
        if val2<val1:    
            print('Erreur ligne',line_num(ip),':',val1,'et',val2,'ne définissent par des bornes cohérentes pour un tirage aléatoire')
            return -1
        int_vars[dest]=random.randint(val1,val2)
        if trace:
            print(line_num(ip),'- Tirage au hasard entre',val1,'et',val2,'dans la variable entière',dest)
    return ip+1
    
def parse_random_instr(ip,tokens,skip):
    if tokens[0]=='tirer':
        if len(tokens)!=8 or tokens[2]!='au' or tokens[3]!='hasard' or tokens[4]!='entre' or tokens[6]!='et':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de tirage aléatoire incorrecte')
            return -1
        if not assert_var_def(ip,tokens[1]):
            return -1
        if is_int_var(tokens[1]):
            return do_int_random(ip,tokens[5],tokens[7],tokens[1],skip)
        print('Erreur ligne',line_num(ip),': type incorrect pour la variable d\'affectation')
        return -1
    else:
        return -1

def parse_write_instr(ip,tokens,skip):
    if tokens[0]=='écrire':
        if not skip:
            no_cr=False
            sep_char=' '
            for i in range(1,len(tokens)):
                if tokens[i][0]!='$':
                    if tokens[i][0]!='@':
                        if i==len(tokens)-1 and tokens[i]=='pdrc':
                            no_cr=True
                        else:
                            if i==1 and tokens[i]=='pdsép':
                                sep_char=''
                            else:
                                print(tokens[i],'',sep=sep_char,end='')
                    else:
                        varname=tokens[i].split('@')[1]
                        if not assert_var_def(ip,varname):
                            return -1
                        if not is_int_var(varname):
                            print('Erreur ligne',line_num(ip),': variable non entière utilisée avec opérateur @')
                            return -1
                        print(int_to_char(int_vars[varname]),'',sep=sep_char,end='')
                else:
                    varname=tokens[i].split('$')[1]
                    if not assert_var_def(ip,varname):
                        return -1
                    if is_int_var(varname):
                        print(int_vars[varname],'',sep=sep_char,end='')
                    if is_bool_var(varname):
                        print(bool_to_str(bool_vars[varname]),'',sep=sep_char,end='')
            if not no_cr:
                print()
            if trace:
                print(line_num(ip),'- Ecriture ci-dessus')
        return ip+1
    else:
        return -1

def parse_halt_instr(ip,tokens,skip):
    if tokens[0]=='arrêter':
        if len(tokens)!=1:
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction d\'arrêt incorrecte')
            return -1
        if not skip:
            if trace:
                print(line_num(ip),'- Instruction d\'arrêt')
            end_exec()
        return ip+1
                
    else:
        return -1

def parse_assert_instr(ip,tokens,skip):
    if tokens[0]=='vérifier':
        if len(tokens)!=2:
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de vérification incorrecte')
            return -1
        if not check_bool_value(tokens[1]):
            print('Erreur ligne',line_num(ip),':',tokens[1],'n\'est pas une opérande valide pour une vérification')
            return -1
        if not skip:
            val=get_bool_value(tokens[1])
            if trace:
                print(line_num(ip),'- Instruction de vérification sur la valeur',val)
            if not val:
                print('Condition ligne',line_num(ip),'non vérifiée !')
                end_exec()
        return ip+1
    else:
        return -1

def parse_instr_block(ip,skip):
    new_ip=ip
    while True: 
        if new_ip>=len(program):
            print('Erreur ligne',line_num(new_ip),': pas de fin trouvée pour le block initié à la ligne',line_num(ip-1),'...')
            return -1
        if len(program[new_ip].split())>0:
            if program[new_ip].split()[0]=='fin':
                break;
        new_ip=exec_line(new_ip,skip)
        if new_ip==-1:
            return -1
    return new_ip

# pour <var> de <var|val> à <var|val> faire
#     ...
# fin
def parse_for_instr(ip,tokens,skip):
    if tokens[0]=='pour':
        if len(tokens)!=7 or tokens[2]!='de' or tokens[4]!='à' or tokens[6]!='faire':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de bouclage \'pour\' incorrecte')
            return -1
        if not check_label(tokens[1]):
            print('Erreur ligne',line_num(ip),':',tokens[1],'n\'est pas un nom de variable valide')
            return -1
        if not is_defined(tokens[1]):
            print('Erreur ligne',line_num(ip),': la variable',tokens[1],'n\'est pas définie')
            return -1
        if not is_int_var(tokens[1]):
            print('Erreur ligne',line_num(ip),': la variable',tokens[1],'n\'est pas un entier')
            return -1        
        if not check_int_value(tokens[3]):
            print('Erreur ligne',line_num(ip),':',tokens[3],'n\'est pas une borne de boucle valide')
            return -1
        if not check_int_value(tokens[5]):
            print('Erreur ligne',line_num(ip),':',tokens[5],'n\'est pas une borne de boucle valide')
            return -1
        new_ip=0
        if skip:
            new_ip=parse_instr_block(ip+1,skip)
            if new_ip==-1:
                return -1
        else:
            lower_bound=get_int_value(tokens[3])
            upper_bound=get_int_value(tokens[5])
            if upper_bound<lower_bound:
                print('Erreur ligne',line_num(ip),':',tokens[3],'et',tokens[5],'ne définissent par des bornes de boucle cohérentes')
                return -1
            if trace:
                print(line_num(ip),'- Bouclage sur',tokens[1],'de',lower_bound,'à',upper_bound)
            new_ip=-1
            for i in range(lower_bound,upper_bound+1):
                int_vars[tokens[1]]=i
                new_ip=parse_instr_block(ip+1,skip)
                if new_ip==-1:
                    print('Interruption boucle de la ligne',line_num(ip))
                    return -1
        return new_ip+1
    else:
        return -1
            
def parse_while_instr(ip,tokens,skip):
    if len(tokens)<2:
        return -1
    if tokens[0]=='tant' and tokens[1]=='que':
        if len(tokens)!=4 or tokens[3]!='faire':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de bouclage \'tant que\' incorrecte')
            return -1
        if not check_bool_value(tokens[2]):
            print('Erreur ligne',line_num(ip),':',tokens[2],'n\'est pas une condition de boucle valide')
            return -1
        new_ip=0
        if skip:
            new_ip=parse_instr_block(ip+1,skip)
            if new_ip==-1:
                return -1
        else:
            if not get_bool_value(tokens[2]):
                # Then we still need to parse the loop body but with skipping on.
                new_ip=parse_instr_block(ip+1,True)
                if new_ip==-1:
                    return -1                
            else:
                if trace:
                    print(line_num(ip),'- Bouclage sur',tokens[2])                
                while get_bool_value(tokens[2]):
                    new_ip=parse_instr_block(ip+1,skip)
                    if new_ip==-1:
                        print('Interruption boucle de la ligne',line_num(ip))
                        return -1            
        return new_ip+1
    else:
        return -1

def parse_if_instr(ip,tokens,skip):
    if tokens[0]=='si':
        if len(tokens)!=3 or tokens[2]!='alors':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction conditionnelle \'si\' incorrecte')
            return -1
        if not check_bool_value(tokens[1]):
            print('Erreur ligne',line_num(ip),':',tokens[1],'n\'est pas une condition valide')
            return -1
        new_ip=0
        if skip:
            new_ip=parse_instr_block(ip+1,skip)
            if new_ip==-1:
                return -1
        else:
            if not get_bool_value(tokens[1]):
                if trace:
                    print(line_num(ip),'- Condition sur',tokens[1],'à faux')            
                # Then we still need to parse the if body but with skipping on.
                new_ip=parse_instr_block(ip+1,True)
                if new_ip==-1:
                    return -1                
            else:
                if trace:
                    print(line_num(ip),'- Condition sur',tokens[1],'à vrai')            
                new_ip=parse_instr_block(ip+1,skip)
                if new_ip==-1:
                    print('Interruption si de la ligne',line_num(ip))
                    return -1            
        return new_ip+1
    else:
        return -1

def parse_proc_instr(ip,tokens,skip):
    if tokens[0]=='procédure':
        if len(tokens)!=3 or tokens[2]!='début':
            print('Erreur ligne',line_num(ip),': syntaxe de déclaration de procédure incorrecte')
            return -1
        if not check_label(tokens[1]):
            print('Erreur ligne',line_num(ip),':',tokens[1],'n\'est pas un nom de procédure valide')
            return -1
        if is_proc_defined(tokens[1]):
            print('Erreur ligne',line_num(ip),': une procédure',tokens[1],'est déjà définie')
            return -1
        # If we're not skipping, just add ip+1 in the proc_table.
        if not skip:
            proc_table[tokens[1]]=ip+1
            if trace:
                print(line_num(ip),'- Définition de la procédure',tokens[1],'@',ip+1)
        # Then, regardless of skip value we skip over the proc body (procs are executed when they're called).
        new_ip=parse_instr_block(ip+1,True)
        if new_ip==-1:
            return -1
        return new_ip+1
    else:
        return -1        
        
def parse_call_instr(ip,tokens,skip):
    if tokens[0]=='appeler':
        if len(tokens)!=2:
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction d\'appel de procédure incorrecte')
            return -1
        if not check_label(tokens[1]):
            print('Erreur ligne',line_num(ip),':',tokens[1],'n\'est pas un nom de procédure valide')
            return -1
        if not is_proc_defined(tokens[1]):
            print('Erreur ligne',line_num(ip),': la procédure',tokens[1],'n\'est pas définie')
            return -1
        if not skip:
            if trace:
                print(line_num(ip),'- Appel de la procédure',tokens[1])            
            # Then we execute the block at the address in the proc table.
            new_ip=parse_instr_block(proc_table[tokens[1]],False)
            if new_ip==-1:
                return -1                
            if trace:
                print(line_num(ip),'- Retour d\'appel de la procédure',tokens[1])            
        return ip+1 # In all cases, once we're done, we jump to the instruction following the call.
    else:
        return -1

def parse_dict_instr(ip,tokens,skip):
    if tokens[0]=='dictionnaire':
        if len(tokens)!=2:
            print('Erreur ligne',line_num(ip),': syntaxe de déclaration incorrecte d\'un dictionnaire')
            return -1
        if not check_label(tokens[1]):
            print('Erreur ligne',line_num(ip),':',tokens[1],'n\'est pas un nom de variable valide')
            return -1
        if is_defined(tokens[1]):
            print('Erreur ligne',line_num(ip),': une variable',tokens[1],'est déjà définie')
            return -1
        if not skip:
            dict_vars[tokens[1]]=dict()
            if trace:
                print(line_num(ip),'- Définition du dictionnaire',tokens[1],'(initialisé à vide)')
        return ip+1
    else:
        return -1

def do_int_insert(ip,key,val,dest,skip):
    if not check_int_value(key):
        print('Erreur ligne',line_num(ip),':',key,'n\'est pas une clef d\'insertion valide pour un dictionnaire')
        return -1
    if not check_int_value(val):
        print('Erreur ligne',line_num(ip),':',val,'n\'est pas une valeur d\'insertion valide pour un dictionnaire')
        return -1
    if not skip:
        key_as_int=get_int_value(key)
        val_as_int=get_int_value(val)
        dict_vars[dest][key_as_int]=val_as_int
        if trace:
            print(line_num(ip),'- Association/insertion de la clef',key_as_int,'à la valeur',val_as_int,'dans le dictionnaire',dest)
    return ip+1

def parse_insert_instr(ip,tokens,skip):
    if tokens[0]=='insérer':
        if len(tokens)!=4 or tokens[2]!='dans':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction d\'insertion incorrecte')
            return -1
        if not assert_var_def(ip,tokens[3]):
            return -1
        if not is_dict_var(tokens[3]):
            print('Erreur ligne',line_num(ip),': la variable',tokens[3],'n\'est pas un dictionnaire')
            return -1
        return do_int_insert(ip,tokens[1],'0',tokens[3],skip)
    else:
        return -1

def parse_bind_instr(ip,tokens,skip):
    if tokens[0]=='associer':
        if len(tokens)!=6 or (tokens[2]!='à' and tokens[2]!='avec') or tokens[4]!='dans':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction d\'association incorrecte')
            return -1
        if not assert_var_def(ip,tokens[5]):
            return -1
        if not is_dict_var(tokens[5]):
            print('Erreur ligne',line_num(ip),': la variable',tokens[5],'n\'est pas un dictionnaire')
            return -1
        return do_int_insert(ip,tokens[1],tokens[3],tokens[5],skip)
    else:
        return -1

def do_int_access(ip,source,key,dest,skip):
    if not check_int_value(key):
        print('Erreur ligne',line_num(ip),':',key,'n\'est pas une clef valide pour accéder à',source)
        return -1
    if not skip:
        key_as_int=get_int_value(key)
        if not key_as_int in dict_vars[source]:
            print('Erreur ligne',line_num(ip),':',key,'n\'est pas une clef présente dans',source)
            return -1
        int_vars[dest]=dict_vars[source][key_as_int]
        if trace:
            print(line_num(ip),'- Accès à',source,'avec la clef',key,' dans la variable entière',dest)
    return ip+1
       
def parse_access_instr(ip,tokens,skip):
    if tokens[0]=='accéder':
        if len(tokens)!=6 or tokens[2]!='avec' or tokens[4]!='dans':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction d\'accès incorrecte')
            return -1
        if not assert_var_def(ip,tokens[1]):
            return -1
        if not is_dict_var(tokens[1]):
            print('Erreur ligne',line_num(ip),': la variable',tokens[5],'n\'est pas un dictionnaire')
            return -1
        if not assert_var_def(ip,tokens[5]):
            return -1
        if is_int_var(tokens[5]):
            return do_int_access(ip,tokens[1],tokens[3],tokens[5],skip)
        print('Erreur ligne',line_num(ip),': type incorrect pour la variable d\'affectation')
        return -1
    else:
        return -1

def do_bool_search(ip,source,key,dest,skip):
    if not check_int_value(key):
        print('Erreur ligne',line_num(ip),':',key,'n\'est pas une clef valide pour chercher dans',source)
        return -1
    if not skip:
        key_as_int=get_int_value(key)
        bool_vars[dest]=key_as_int in dict_vars[source]
        if trace:
            print(line_num(ip),'- Recherche dans',source,'avec la clef',key,'dans la variable booléenne',dest)
    return ip+1

def parse_search_instr(ip,tokens,skip):
    if tokens[0]=='rechercher':
        if len(tokens)!=6 or tokens[2]!='avec' or tokens[4]!='dans':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de recherche incorrecte')
            return -1
        if not assert_var_def(ip,tokens[1]):
            return -1
        if not is_dict_var(tokens[1]):
            print('Erreur ligne',line_num(ip),': la variable',tokens[5],'n\'est pas un dictionnaire')
            return -1
        if not assert_var_def(ip,tokens[5]):
            return -1
        if is_bool_var(tokens[5]):
            return do_bool_search(ip,tokens[1],tokens[3],tokens[5],skip)
        print('Erreur ligne',line_num(ip),': type incorrect pour la variable d\'affectation')
        return -1
    else:
        return -1

def do_remove(ip,key,dest,skip):
    if not check_int_value(key):
        print('Erreur ligne',line_num(ip),':',key,'n\'est pas une clef valide pour une suppression de dictionnaire')
        return -1
    if not skip:
        key_as_int=get_int_value(key)
        if not key_as_int in dict_vars[dest]:
            print('Erreur ligne',line_num(ip),':',key_as_int,'n\'est pas une clef présente dans',dest)
            return -1
        del dict_vars[dest][key_as_int]
        if trace:
            print(line_num(ip),'- Suppression de la clef',key_as_int,'du dictionnaire',dest)
    return ip+1
                
def parse_remove_instr(ip,tokens,skip):
    if tokens[0]=='supprimer':
        if len(tokens)!=4 or tokens[2]!='de':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de suppression incorrecte')
            return -1
        if not assert_var_def(ip,tokens[3]):
            return -1
        if not is_dict_var(tokens[3]):
            print('Erreur ligne',line_num(ip),': la variable',tokens[3],'n\'est pas un dictionnaire')
            return -1
        return do_remove(ip,tokens[1],tokens[3],skip)
    else:
        return -1

def parse_on_instr(ip,tokens,skip):
    if tokens[0]=='sur':
        if len(tokens)!=6 or tokens[1]!='tout' or tokens[3]!='de' or tokens[5]!='faire':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction d\'itération sur dictionnaire incorrecte')
            return -1
        if not check_label(tokens[2]):
            print('Erreur ligne',line_num(ip),':',tokens[2],'n\'est pas un nom de variable valide')
            return -1
        if not is_defined(tokens[2]):
            print('Erreur ligne',line_num(ip),': la variable',tokens[2],'n\'est pas définie')
            return -1
        if not is_int_var(tokens[2]):
            print('Erreur ligne',line_num(ip),': la variable',tokens[2],'n\'est pas un entier')
            return -1        
        if not check_label(tokens[4]):
            print('Erreur ligne',line_num(ip),':',tokens[4],'n\'est pas un nom de variable valide')
            return -1
        if not is_defined(tokens[4]):
            print('Erreur ligne',line_num(ip),': la variable',tokens[4],'n\'est pas définie')
            return -1
        if not is_dict_var(tokens[4]):
            print('Erreur ligne',line_num(ip),': la variable',tokens[4],'n\'est pas un dictionnaire')
            return -1        
        new_ip=0
        if skip:
            new_ip=parse_instr_block(ip+1,skip)
            if new_ip==-1:
                return -1
        else:
            if len(dict_vars[tokens[4]])==0:
                new_ip=parse_instr_block(ip+1,True)
                if new_ip==-1:
                    return -1
            else:
                if trace:
                    print(line_num(ip),'- Bouclage sur les éléments de',tokens[4],'dans',tokens[2])
                for i in sorted(dict_vars[tokens[4]]):
                    int_vars[tokens[2]]=i
                    new_ip=parse_instr_block(ip+1,skip)
                    if new_ip==-1:
                        print('Interruption boucle de la ligne',line_num(ip))
                        return -1
        return new_ip+1
    else:
        return -1

loop_t0=time.time()           
tenths_ctr=0
period_duration_in_tenths=0

def delayUntilNextPeriod():
    global tenths_ctr,loop_t0
    tenths_ctr=tenths_ctr+period_duration_in_tenths
    t=time.time()-loop_t0
    delay=tenths_ctr/10-t
    if delay<0:
        return -1
    time.sleep(delay)
                
def parse_realtime_instr(ip,tokens,skip):
    global loop_t0,period_duration_in_tenths
    if len(tokens)<2:
        return -1
    if tokens[0]=='tous' and tokens[1]=='les':
        if len(tokens)!=5 or tokens[3]!='dixièmes' or tokens[4]!='faire':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de bouclage temps réel incorrecte')
            return -1
        if not check_int_value(tokens[2]):
            print('Erreur ligne',line_num(ip),':',tokens[2],'n\'est pas une valeur de période valide')
            return -1
        new_ip=0
        if skip:
            new_ip=parse_instr_block(ip+1,skip)
            if new_ip==-1:
                return -1
        else:
            # A real-time loop never ends.
            period_duration_in_tenths=get_int_value(tokens[2])
            loop_t0=time.time()
            if period_duration_in_tenths<1:
                print('Erreur ligne',line_num(ip),'la période d\'une boucle temps réel doit être >= 1 dixième')
                return -1
            if trace:
                print(line_num(ip),'Démarrage boucle temps réel de période',period_duration_in_tenths,'dixièmes à',t0)
            if delayUntilNextPeriod()==-1:
                print('Erreur ligne',line_num(ip),'violation d\'échéance temps réel sur 1ère itération')
                return -1
            while True:
                if trace:
                    print(line_num(ip),'Exécution corps de boucle temps réel à',time.time()-t0)
                new_ip=parse_instr_block(ip+1,skip)
                if new_ip==-1:
                    print('Interruption boucle de la ligne',line_num(ip))
                    return -1
                if delayUntilNextPeriod()==-1:
                    print('Erreur ligne',line_num(ip),'violation d\'échéance temps réel')
                    return -1
    return -1

t0_prog=time.time()

def get_exe_time():
    t=time.time();
    return int(round(10.0*(t-t0_prog)))
        
def print_exe_time():
    print('Temps d\'exécution :',get_exe_time(),'dixièmes')

def parse_chrono_instr(ip,tokens,skip):
    if tokens[0]=='chronométrer':
        if len(tokens)!=3 or tokens[1]!='dans':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de chronométrage incorrecte')
            return -1
        if not assert_var_def(ip,tokens[2]):
            return -1
        if not skip:
            if is_int_var(tokens[2]):
                val=get_exe_time()
                int_vars[tokens[2]]=int(val)
                if trace:
                    print(line_num(ip),'- Chronométrage du temps d\'exécution dans l\'entier',tokens[1])
        return ip+1
    else:
        return -1

def parse_delay_instr(ip,tokens,skip):
    if tokens[0]=='temporiser':
        if len(tokens)!=4 or tokens[1]!='de' or tokens[3]!='dixièmes':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction de temporisation incorrecte')
            return -1
        if not check_int_value(tokens[2]):
            print('Erreur ligne',line_num(ip),':',tokens[2],'n\'est pas une valeur de temporisation valide')
            return -1
        if not skip:
            delay=get_int_value(tokens[2])
            if delay<0:
                print('Erreur ligne',line_num(ip),': valeur de temporisation négative')
            time.sleep(delay/10.0)
            if trace:
                print(line_num(ip),'- Temporisation de',delay,'dixièmes à',get_exe_time(),'dixièmes')
        return ip+1
    else:
        return -1
        
def exec_line(ip,skip):
    tokens=program[ip].split()
    if len(tokens)==0:
# Let's not trace empty lines.
#        if trace:
#            print(line_num(ip),'- Ligne vide')
        return ip+1
    else:
        if tokens[0]=='$' or tokens[0]=='#':
# Let's not trace comments as well.
#            if trace:
#                print(line_num(ip),'- Ligne de commentaires')
            return ip+1
        new_ip=parse_int_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_bool_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_read_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_show_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_assign_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_add_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_mul_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_sub_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_div_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_mod_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_pow_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_max_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_min_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_cmp_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_neq_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_lower_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_upper_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_disj_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_conj_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_comp_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_random_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_write_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_halt_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip            
        new_ip=parse_assert_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip            
        new_ip=parse_if_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_for_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_while_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_proc_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_call_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_dict_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_insert_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_bind_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_access_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_search_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_remove_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_on_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_realtime_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_chrono_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        new_ip=parse_delay_instr(ip,tokens,skip)
        if new_ip!=-1:
            return new_ip
        print('Erreur à la ligne',line_num(ip),': instruction inconnue ou séquence interrompue')
        return -1
    return -1

def end_exec():
    print()
    print('Fin de l\'exécution')
    print()
    if trace:
        print_memory()
        print()
    if chrono:
        print_exe_time()
        print()
    if interactive:
        x=input('Appuyer sur Entrée pour fermer...')
    sys.exit(1)
    
def exec_program():
    print('Démarrage de l\'exécution')
    print()
    ip=0;
    while ip<len(program) and ip>=0:
        ip=exec_line(ip,False)
    end_exec()
        
print('Orvet version',version)

if len(sys.argv)<2:
    print('Utilisation :',sys.argv[0],'[fichier].orv -trace (optionnel) -non-interactif (optionnel) -chrono (optionnel)')
    sys.exit(1)

try:    
    load_program(sys.argv[1])
except FileNotFoundError:
    print('Le fichier',sys.argv[1],'semble ne pas exister !')
    sys.exit(1)

if len(sys.argv)>2:
    for i in range(2,len(sys.argv)):
        unknown_option=True
        if sys.argv[i]=='-trace':
            trace=True
            unknown_option=False
        if sys.argv[i]=='-non-interactif':
            interactive=False
            unknown_option=False
        if sys.argv[i]=='-chrono':
            chrono=True
            unknown_option=False
        if unknown_option:
            print('Option inconnue :',sys.argv[2],'(ignorée)')

# print_program()

try:
    t0_prog=time.time()
    exec_program()
except KeyboardInterrupt:
    print('\nInterruption utilisateur !')
    end_exec()
except RuntimeError as err:
    print('\nErreur d\'exécution Python :-(')
    print('\nMessage d\'erreur Python :',err)
    end_exec()
except EOFError as err:
    print('\nErreur d\'entrées/sortie Python :-(')
    print('\nMessage d\'erreur Python :',err)
    interactive=False
    end_exec()
    

