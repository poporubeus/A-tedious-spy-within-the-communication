from qkd_class import qkd

shots=20

n = 10
nmin = 3
nmax = 30
shot_list=[2,4,10]

def plot_results(arg):
  if arg == shots:
    res_single_shot = qkd(n,nmin,nmax,shots,shot_list)
    res_single_shot = res_single_shot.simul()
    return res_single_shot
  elif arg == shot_list:
    res_multiple_shots = qkd(n,nmin,nmax,shots,shot_list)
    res_multiple_shots = res_multiple_shots.simul_w_many_shots()
    return res_multiple_shots

if __name__ == '__main__':
  plot = plot_results(arg=shot_list) 