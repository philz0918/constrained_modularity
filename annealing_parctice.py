## we're doing lnversely
initial_temp = 40 
cooling_constant = 1.0015

modul_old = 0.335
modul_new = 0.230

## max number of iteration is 10000

for i in range(10000) :
    
    modul_old 
    temp = new_temp(initial_temp, i)
    
    
    ##why we need rejection threshold?

   
    acceptance = False
    while acceptance is False :
        
        if no modularity, old modularity is None  :
            get modularty from initial/grouping 
            new modularity -> old modularity
            
          
        
        point patch = get new partition
        and get new modularity with new partition 
        new temp
        
        ## we only need point pitch since we constrained number of groups
    
        get_modularity of new grouping
        
        check accpetance 
        acceptance = check_acceptance(modul_old, modul_new, temp)
        
        if acceptance is True:
            
            saving groups in savinv_group_list
            if not saving_group is None :
                if grouping is unique
                 adding up
                else 
                acceptance = False
            
#inverse annealing