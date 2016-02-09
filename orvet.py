
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

version='0.1'
program=[]
int_vars=dict()
bool_vars=dict()
trace=False

def load_program(prog_name):
    l=0
    print('Chargement du programme')
    with open(prog_name) as file:
        for line in file:
            program.append(line)
            l=l+1
    print(l,'lignes chargées')
    file.close()
        
    
def print_program():
    l=0
    print('Programme :')
    for line in program:
        print(l,'-',line,end='')
        l=l+1

def print_int_vars():
    print('Entiers :')
    for var,val in sorted(int_vars.items()):
        print(var,'=',val)

def bool_to_str(b):
    if b==True:
        return 'vrai'
    return 'faux'
        
def print_bool_vars():
    print('Booléens :')
    for var,val in sorted(bool_vars.items()):
        print(var,'=',bool_to_str(val))
        
def print_memory():
    print('Mémoire :')
    print_int_vars()
    print_bool_vars()

def check_label(token):
#    if not token.isalnum():
#        return False
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
    
def is_defined(var):
    if is_int_var(var):
        return True
    if is_bool_var(var):
        return True
    return False
    
def is_int_var(var):
    if var in int_vars:
        return True
    return False

def is_bool_var(var):
    if var in bool_vars:
        return True
    return False
    
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
                val=input('Valeur de l\'entier '+tokens[1]+' ? ')
                while not check_int(val):
                    print('Ce n\'est pas un entier !')
                    val=input('Valeur de l\'entier '+tokens[1]+' ? ')
                int_vars[tokens[1]]=int(val)
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
        if len(tokens)!=4 or tokens[2]!='à':
            print('Erreur ligne',line_num(ip),': syntaxe d\'instruction d\'affectation incorrecte')
            return -1
        if not assert_var_def(ip,tokens[3]):
            return -1
        if is_int_var(tokens[3]):
            return do_int_assign(ip,tokens[1],tokens[3],skip)
        if is_bool_var(tokens[3]):
            return do_bool_assign(ip,tokens[1],tokens[3],skip)        
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
        if len(tokens)!=6 or tokens[2]!='à' or tokens[4]!='dans':
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
        if len(tokens)!=6 or tokens[2]!='par' or tokens[4]!='dans':
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
        if len(tokens)!=6 or tokens[2]!='avec' or tokens[4]!='dans':
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
        if len(tokens)!=6 or tokens[2]!='avec' or tokens[4]!='dans':
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
        if len(tokens)!=6 or tokens[2]!='et' or tokens[4]!='dans':
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
        if len(tokens)!=6 or tokens[2]!='et' or tokens[4]!='dans':
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
            for i in range(1,len(tokens)):
                if tokens[i][0]!='$':
                    print(tokens[i],'',end='')
                else:
                    varname=tokens[i].split('$')[1]
                    if not assert_var_def(ip,varname):
                        return -1
                    if is_int_var(varname):
                        print(int_vars[varname],'',end='')
                    if is_bool_var(varname):
                        print(bool_to_str(bool_vars[varname]),'',end='')
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
        print('Erreur à la ligne',line_num(ip),': instruction inconnue ou séquence interrompue')
        return -1
    return -1

def end_exec():
    print()
    print('Fin de l\'exécution')
    if trace:
        print_memory()
    print()
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
    print('Utilisation :',sys.argv[0],'[fichier].orv -trace (optionel)')
    sys.exit(1)

try:    
    load_program(sys.argv[1])
except FileNotFoundError:
    print('Le fichier',sys.argv[1],'semble ne pas exister !')
    sys.exit(1)

if len(sys.argv)==3:
    if sys.argv[2]=='-trace':
        trace=True
    else:
        print('Option inconnue :',sys.argv[2],'(ignorée)')

# print_program()

try:
    exec_program()
except KeyboardInterrupt:
    print('\nInterruption utilisateur !')
    end_exec()



