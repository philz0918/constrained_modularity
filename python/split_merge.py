#split and merge for over 3 
def splandmer(group_list,cn) :
    #print("split ing..", group_list)
    
    
    num_of_elements = 0 
    
    while num_of_elements == 0 or num_of_elements == 2 or num_of_elements == 1 :
        
        #print("Here...")
        group_list.sort()
    
        n_groups = cn 
    
        # set the group 
        set_group = list(set(group_list))
        
        for element in set_group :
            
            if group_list.count(element) == 1 :
                #print(group_list.count(element))
                num_of_elements = 1
                continue
            elif group_list.count(element) == 2 :
                num_of_elements = 2
                continue
        
        #check the number of elements(not 1 or 2)
        # choice for group to be spilit and merge 
        rand_choice = random.choice(set_group)
            
        # get the list of splited and merged group
        gr_change = [y for y in group_list if y == rand_choice]
    
        #get a lenght for selected 
        num_selected = group_list.count(rand_choice)
        
        # 1 or 2 selected groups cannot be handle here (1 can make void group, 2 is single movement(local movement))
        if num_selected == 1 :
            num_of_elements =1
            continue
        elif num_selected == 2:
            num_of_elements = 2
            continue
            
        #select number that change elments
        #we should not choose the maximum number of selected group -> it means one group disappear
        
        change = random.choice([i+1 for i in range(num_selected-1)])
    
        #spliting group 
        split_gr = random.sample(gr_change, change)
    
        #choose group to merge into
        merge_gr = random.choice([z for z in range(cn) if z != rand_choice])
    
        #merging
        cnt = 0
        
        for idx, val in enumerate(group_list) :
            if val == rand_choice :
                #len(split_gr) = number of elements should be changed
                if cnt <len(split_gr) :
                    group_list[idx] = merge_gr
                    cnt +=1
                else : 
                    break
        break
    
    new_group_list = group_list
    
    return new_group_list
    