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


    def calculate_rejection_threshold(self,n,c):
        """Uses the COUPON COLLECTOR criterion to terminate
           at a local optimum with high probability."""

        number_of_individual_moves = n*c

        if self.mergesplit_on:
            number_of_split_moves = c
            number_of_merge_moves = c*(c-1)/2
            number_of_moves = number_of_individual_moves + number_of_split_moves + number_of_merge_moves
            self.merge_probability = float(number_of_merge_moves) / number_of_moves
            self.split_probability = float(number_of_split_moves) / number_of_moves
        else:
            number_of_moves = number_of_individual_moves
            self.merge_probability = 0
            self.split_probability = 0
        
        # We want a 95% confidence
        beta = 1 - math.log(0.05)/math.log(number_of_moves)
        
        return beta*number_of_moves*math.log(number_of_moves)