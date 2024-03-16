# The name of the task you want to calculate

list=("household1"
"household2"
"household3"
"household4"
"household5"
"household6"
"household7"
"household8"
"household9"
"household10")

# list=("cooking1"
# "cooking2"
# "cooking3"
# "cooking4"
# "cooking5"
# "cooking6"
# "cooking7"
# "cooking8"
# "cooking9"
# "cooking10")

# list=("lab1"
# "lab2" 
# "lab3"
# "lab4"
# "lab5"
# "lab6"
# "lab7"
# "lab8"
# "lab9"
# "lab10")

# list=('household1,household2' 
# 'household2,household3'  
# 'household3,household4' 
# 'household4,household5' 
# 'household5,household6' 
# 'household6,household7' 
# 'household7,household8'
# 'household8,household9'
# 'household9,household10'
# 'household10,household1')

# list=('cooking1,cooking2'
# 'cooking2,cooking3'  
# 'cooking3,cooking4' 
# 'cooking4,cooking5' 
# 'cooking5,cooking6' 
# 'cooking6,cooking7' 
# 'cooking7,cooking8' 
# 'cooking8,cooking9' 
# 'cooking9,cooking10'
# 'cooking10,cooking1')

# list=('lab1,lab2' 
# 'lab2,lab3' 
# 'lab3,lab4' 
# 'lab4,lab5' 
# 'lab5,lab6' 
# 'lab6,lab7' 
# 'lab7,lab8' 
# 'lab8,lab9' 
# 'lab9,lab10'
# 'lab10,lab1')

# list=('household1,household2,household3'
# 'household2,household3,household4'
# 'household3,household4,household5'
# 'household4,household5,household6'
# 'household5,household6,household7'
# 'household6,household7,household8'
# 'household7,household8,household9'
# 'household8,household9,household10'
# 'household9,household10,household1'
# 'household10,household1,household2')

# list=('cooking1,cooking2,cooking3'
# 'cooking2,cooking3,cooking4'
# 'cooking3,cooking4,cooking5'
# 'cooking4,cooking5,cooking6'
# 'cooking5,cooking6,cooking7'
# 'cooking6,cooking7,cooking8'
# 'cooking7,cooking8,cooking9'
# 'cooking8,cooking9,cooking10'
# 'cooking9,cooking10,cooking1'
# 'cooking10,cooking1,cooking2')

# list=('lab1,lab2,lab3'
# 'lab2,lab3,lab4'
# 'lab3,lab4,lab5'
# 'lab4,lab5,lab6'
# 'lab5,lab6,lab7'
# 'lab6,lab7,lab8'
# 'lab7,lab8,lab9'
# 'lab8,lab9,lab10'
# 'lab9,lab10,lab1'
# 'lab10,lab1,lab2') 


for item in "${list[@]}"
do
    python LLM_test.py --taskName $item --lm gpt3.5 --total_time 40 --save_path ./trajectory/single --save_name $item
    # python LLM_test.py --taskName $item --lm mistral --total_time 40 --save_path ./trajectory/single --save_name $item --model_name ../hf_model/Mistral-7B-Instruct-v0.2 --ip http://localhost --port 8090
done
