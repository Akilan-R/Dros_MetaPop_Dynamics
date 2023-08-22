import numpy as np


##define the fixed parameters
hatchability = 0.98  #if hatchability is density (egg or adult) depedent, then define it in the pre-adult-module or the adult-module functions 
x1 = 2.5  #parameter in finding the mean larval size
x2 = 1  #parameter in finding the mean larval size 
x3 = 0.009 #parameter in finding the mean larval size 
sigma_size = 0.45  #parameter in assigning larval sizes by drawing from a normal distribution
mc = 1.1 #critical size cut off of the larval stage for successful pupation (= 1.1 (JB) and 1 (FEJ))
x4 = 1.0  #parameter in finding the adult sizes
female_proportion = 0.5 #assign sex to the adutls 
x5 = 85 #parameter in finding fecundity
x6 = 2  #parameter in finding fecundity
sen_adsize = 1.7 #parameter related to sensitivity of fecundity to adult size
sen_adden = 0.17 #parameter related to sensivity of fecundity to adult denisity


##Pre-Adult-Module
#food = larval food amt; 1.76 (LL and LH), 2.56 (HL and HH) 
def Pre_Adult_Module(numegg,food):
    numlarva = int(hatchability*numegg)
    mean_size = x1*(1-1/(x2+np.exp(-x3*numlarva+food)))
    size_larva_arr = np.random.normal(mean_size, sigma_size, numlarva)
    numadult = (size_larva_arr>=mc).sum()
    size_adult_arr = x4*size_larva_arr[size_larva_arr>=mc]
    return numadult, size_adult_arr

##Adult-Module
#adnut = #adult nutrition quality; 1 (LL and HL), 1.29 (HH) and 1.49 (LH)
def Adult_Module(numadult, size_adult_arr,adnut):
    adult_sex_arr = np.random.binomial(size=numadult, n=1, p=female_proportion) # 1 is a female and 0 a male
    size_female_arr = size_adult_arr[adult_sex_arr == 1]
    addens_ind_fec_arr = adnut*x5*np.log(x6+sen_adsize*size_female_arr)
    addens_eff = 1/(1+sen_adden*numadult)
    fecundity_arr = addens_ind_fec_arr*addens_eff
    numegg = fecundity_arr.sum()
    return numegg

##Simulation
def Simulation(numegg,food,adnut,generations,replicates):
    numadult_matrix = np.zeros((generations,replicates)) #array to store the number of adults per generation
    for i in range(replicates):
        # 1st generation, we start with numegg eggs
        numadult, size_adult_arr = Pre_Adult_Module(numegg,food)
        numadult_matrix[0,i] = numadult
        for j in range(1,generations):
            numegg = Adult_Module(numadult,size_adult_arr,adnut)
            numadult, size_adult_arr = Pre_Adult_Module(numegg,food)
            numadult_matrix[j,i] = numadult
    return numadult_matrix



numadult_matrix = Simulation(150,1.76,1,49,8)
