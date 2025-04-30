import math
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 12})
import os, sys,glob,subprocess
from pymulskips import analyze
from matplotlib.ticker import FormatStrFormatter
margin=10
# Extract exponents and coefficients for LaTeX formatting
def sci_notation(value):
    coeff, exponent = f"{value:.3e}".split("e")
    return coeff, int(exponent)

# Data extracted from the excel file from Peter Wellmann "Temperature vs Growth rate.xlsx" 25 November 2020
# gr is in micron/h
data_samples = {}
data_samples['151'] = {'Power': 5.45, 'T_seed_middle': 1986.26, 'T_seed_edge': 0, 'T_source_middle': 1994.14, 'T_source_edge': 1994.14, 'Exp-Growth-Rate': 101}
data_samples['148'] = {'Power': 5.85, 'T_seed_middle': 2040.19, 'T_seed_edge': 0, 'T_source_middle': 2048.12, 'T_source_edge': 2048.12, 'Exp-Growth-Rate': 208}
data_samples['149'] = {'Power': 5.90, 'T_seed_middle': 2046.70, 'T_seed_edge': 0, 'T_source_middle': 2054.63, 'T_source_edge': 2054.63, 'Exp-Growth-Rate': 230}
data_samples['152'] = {'Power': 6.00, 'T_seed_middle': 2059.56, 'T_seed_edge': 0, 'T_source_middle': 2067.51, 'T_source_edge': 2067.51, 'Exp-Growth-Rate': 231}
data_samples['153'] = {'Power': 6.10, 'T_seed_middle': 2072.24, 'T_seed_edge': 0, 'T_source_middle': 2080.20, 'T_source_edge': 2080.20, 'Exp-Growth-Rate': 287}

lenx, leny, lenz = 120, 120, 2400 # Box size --> KMC super-lattice units (0.436/12 nm for SiC-3C)
KMC_lattice_constant = 0.436/12 # nm
box_area =  lenx*leny * (KMC_lattice_constant*1e-7)**2
print('Box area [cm^2]', box_area)
basepath = '/Users/filipporuberto/miniforge3/envs/mulskips_env/MulSKIPS/parser/data-100-0-9117116'

def count_vacancies(dirname):
    # Loop through all files ending with "_v.xyz"
    keys = ['tot', 'SV', 'CV', 'SAV', 'CAV', 'XV']
    vac_counts = {k: [] for k in keys}
    for file_name in glob.glob(dirname+"/*_v.xyz"):
        if file_name!=dirname+"/I00000000_v.xyz":
            # Count occurrences of lines matching "SV" or "CV" or "SAV" or "CAV" or "XV"
            vac_counts['tot'].append(int(subprocess.check_output(f'tail -n +3 "{file_name}" | wc -l', shell=True)))
            # Count occurrences of lines matching "SV"
            vac_counts['SV'].append(int(subprocess.check_output(f'grep "SV" "{file_name}" | wc -l', shell=True)))
            # Count occurrences of lines matching "CV"
            vac_counts['CV'].append(int(subprocess.check_output(f'grep "CV" "{file_name}" | wc -l', shell=True)))
            # Count occurrences of lines matching "SAV"
            vac_counts['SAV'].append(int(subprocess.check_output(f'grep "SAV" "{file_name}" | wc -l', shell=True)))
            # Count occurrences of lines matching "CAV"
            vac_counts['CAV'].append(int(subprocess.check_output(f'grep "CAV" "{file_name}" | wc -l', shell=True)))
            # Count occurrences of lines matching "XV"
            vac_counts['XV'].append(int(subprocess.check_output(f'grep "XV" "{file_name}" | wc -l', shell=True)))
    return {k: np.array(v) for k,v in vac_counts.items()}

# -------------------
randseed = 9117116  # <--- AGGIORNA IN BASE A CHI VUOI ANALIZZARE
newdT = 0 # <--- AGGIORNA IN BASE A CHI VUOI ANALIZZARE
# -------------------

Tseed = data_samples['153']['T_seed_middle'] + newdT  # [°C]
Tsource_0 = data_samples['153']['T_source_middle'] + newdT # [°C]
#dTlist = np.arange(0,105,5) # dT array
dTlist=[100]
#Tsource = Tsource_0 + dTlist
Tsource = [Tsource_0 + dt for dt in dTlist]


gr_KMC = {}
vac_counts = {}
vac_conc = {}
fig,ax = plt.subplots(1,len(dTlist),figsize=(3*len(dTlist),8))
fig2,ax2 = plt.subplots(1,len(dTlist),figsize=(3*len(dTlist),8))

for j, dT in enumerate(dTlist):

    runpath = basepath  # usa direttamente basepath

    if not os.path.exists(runpath):
        print(f"[WARNING] Directory non trovata: {runpath}. Salto dT = {dT}")
        continue

    try:
        gr_KMC[dT] = analyze.analyze_growth_rate(
            runpath,
            bin_size=5.0,
            surface_roughness=20.0,
            plotting=False,
            Nexclude=2,
            method='polyfit'
        )
        surf_height_path = os.path.join(runpath, "surf_height.txt")
        hsurf = np.loadtxt(surf_height_path)
    except Exception as e:
        print(f"[WARNING] Errore su dT = {dT}: {e}. Salto questo punto.")
        continue

   # gr_KMC[dT], hsurf = analyze.analyze_growth_rate(runpath, bin_size=5.0, surface_roughness=20.0, #plotting=False, Nexclude=2, method='polyfit', return_surf_height=True)

    grown_thickness = hsurf[1:]-hsurf[0] # Angstrom
    grown_volume = grown_thickness*1e-8 * box_area # cm3
    vac_counts[dT] = count_vacancies(runpath)
    vac_conc[dT] = {k: v/grown_volume for k,v in vac_counts[dT].items()} # cm-3 

    for kk in vac_conc[dT].keys():
        print('dT', dT, kk, vac_conc[dT][kk][-1], 'cm-3')
        #for k in range(len(grown_volume)):
        #    print('  Iter {}\t{}\t{:.3e} cm-3'.format(k+1, vac_counts[dT][kk][k], vac_conc[dT][kk][k]))
        ax[j].plot(grown_thickness*1e-1, vac_conc[dT][kk], label=kk) # nm, cm-3
        ax2[j].plot(grown_thickness*1e-1, vac_counts[dT][kk], label=kk) # nm, cm-3
    ax[j].legend(loc='upper right', ncols=2)
    ax[j].set_title(r'Sample {} ({:.0f} nm/s)'.format(dT, gr_KMC[dT]/3.6))
    ax[j].set_xlabel('Grown thickness (nm)')
    ax[j].set_ylabel(r'Vacancy concentration (cm$^{-3}$)')
    ax[j].set_ylim([0,ax[j].get_ylim()[1]])
    ax2[j].legend(loc='upper left', ncols=2)
    ax2[j].set_title(r'Sample {} ({:.0f} nm/s)'.format(dT, gr_KMC[dT]/3.6))
    ax2[j].set_xlabel('Grown thickness (nm)')
    ax2[j].set_ylabel(r'Vacancy counts')
    ax2[j].set_ylim([0,ax2[j].get_ylim()[1]])

fig.tight_layout()
fig2.tight_layout()
fig.savefig('vacancy-conc-vs-grown-thickness.pdf')
fig2.savefig('vacancy-counts-vs-grown-thickness.pdf')


# FINAL PLOT
fig, ax1 = plt.subplots(figsize=(6,4))
ax2 = ax1.secondary_xaxis('top', functions=(lambda x: x, lambda x: x))
gr_KMC_nms = np.array(list(gr_KMC.values()))/3.6 # convert from micron/h to nm/s

def myplot(what, color, y0, label):
    ax1.scatter(gr_KMC_nms, what*1e-18, color=color) # , zorder=10, clip_on=False)
    myx = np.linspace(gr_KMC_nms.min()-margin, gr_KMC_nms.max()+margin, 100)
    myfit = np.polyfit(gr_KMC_nms, what, 1)
    a_coeff, a_exp = sci_notation(myfit[0])
    b_coeff, b_exp = sci_notation(myfit[1])
    ax1.text(75, y0, r'$y = {:.3f} \times 10^{{{:d}}} \cdot x + {:.3f} \times 10^{{{:d}}}$'.format(float(a_coeff), a_exp, float(b_coeff), b_exp), color=color)
    myy = np.poly1d(myfit)(myx)
    ax1.plot(myx, myy*1e-18, c=color, ls='--', label=label)
    ax1.set_xlim([gr_KMC_nms.min()-margin, gr_KMC_nms.max()+margin])
    xticks = ax1.get_xticks()
    mytemp = np.interp(xticks, gr_KMC_nms, Tsource)
    ax2.set_xticks(xticks)
    ax2.set_xticklabels(np.round(mytemp,0).astype(int))

#vac_tot = np.array([vac_conc[dT]['tot'][-1] for dT in dTlist])

#CV = np.array([vac_conc[dT]['CV'][-1] for dT in dTlist])

#SV = np.array([vac_conc[dT]['SV'][-1] for dT in dTlist])



#CAV = np.array([vac_conc[dT]['CAV'][-1] for dT in dTlist])
#SAV = np.array([vac_conc[dT]['SAV'][-1] for dT in dTlist])





#myplot(vac_tot, color='k', y0=8.7, label='All')
#myplot(CV, color='r', y0=8.0, label='CV')
#myplot(SV, color='g', y0=7.3, label='SV')

def safe_extract_with_dT(key):
    values = []
    valid_dT = []
    for dT in dTlist:
        if dT in vac_conc and key in vac_conc[dT]:
            values.append(vac_conc[dT][key][-1])
            valid_dT.append(dT)
    return np.array(values), valid_dT

def myplot(what, xdata=None, color='k', y0=None, label=''):
    if xdata is None:
        xdata = gr_KMC_nms
    if len(xdata) != len(what):
        print(f"[WARNING] Plot skipped for {label}: x and y have different lengths ({len(xdata)} vs {len(what)})")
        return
    ax1.scatter(xdata, what * 1e-18, color=color)
    if y0 is not None:
        ax1.axhline(y0 * 1e-18, linestyle='--', color=color, label=label)

# Figure setup
fig, ax1 = plt.subplots()
ax2 = ax1.twiny()  # second x-axis for source temperature

# Plot all vacancy contributions
vac_tot, valid_dT_tot = safe_extract_with_dT('tot')
gr_KMC_nms_tot = np.array([gr_KMC_nms[dTlist.index(dT)] for dT in valid_dT_tot])
myplot(vac_tot, xdata=gr_KMC_nms_tot, color='k', y0=8.7, label='All')

CV, valid_dT_CV = safe_extract_with_dT('CV')
gr_KMC_nms_CV = np.array([gr_KMC_nms[dTlist.index(dT)] for dT in valid_dT_CV])
myplot(CV, xdata=gr_KMC_nms_CV, color='b', y0=2.1, label='CV')

SV, valid_dT_SV = safe_extract_with_dT('SV')
gr_KMC_nms_SV = np.array([gr_KMC_nms[dTlist.index(dT)] for dT in valid_dT_SV])
myplot(SV, xdata=gr_KMC_nms_SV, color='g', y0=4.2, label='SV')

CAV, valid_dT_CAV = safe_extract_with_dT('CAV')
gr_KMC_nms_CAV = np.array([gr_KMC_nms[dTlist.index(dT)] for dT in valid_dT_CAV])
myplot(CAV, xdata=gr_KMC_nms_CAV, color='r', y0=1.3, label='CAV')

SAV, valid_dT_SAV = safe_extract_with_dT('SAV')
gr_KMC_nms_SAV = np.array([gr_KMC_nms[dTlist.index(dT)] for dT in valid_dT_SAV])
myplot(SAV, xdata=gr_KMC_nms_SAV, color='orange', y0=1.1, label='SAV')

# Axis and save
ax1.legend(loc='center left', frameon=False)
ax1.set_xlabel(r'Growth rate (nm/s)')
ax1.set_ylabel(r'Vacancy concentration ($\times 10^{18}$ cm$^{-3}$)')
ax2.set_xlabel(r'Source temperature (°C)')
plt.tight_layout()
plt.savefig('vacancy-vs-GR-FINAL.pdf')
plt.show()

# WRITE IMPORTANT DATA
data = [Tsource, gr_KMC_nms, vac_tot, CV, SV, SAV, CAV]
#np.savetxt('results.txt', np.column_stack(data), delimiter="\t", fmt="%.5e", header="# Tsource (°C)\t #GR (nm/s)\tconc_all (cm-3)\tconc_CV (cm-3)\tconc_SV (cm-3)\tconc_SAV (cm-3)\tconc_CAV (cm-3)", #comments="# Tseed={}°C, randseed={}\n".format(Tseed, randseed))
# Tentativo di salvataggio robusto
def pad_array(arr, target_len):
    if len(arr) == target_len:
        return arr
    elif len(arr) == 0:
        return np.full(target_len, np.nan)
    elif len(arr) < target_len:
        return np.concatenate([arr, np.full(target_len - len(arr), np.nan)])
    else:
        return arr[:target_len]

try:
    ref_len = len(dTlist)
    data = [
        pad_array(np.array(Tsource), ref_len),
        pad_array(gr_KMC_nms, ref_len),
        pad_array(vac_tot, ref_len),
        pad_array(CV, ref_len),
        pad_array(SV, ref_len),
        pad_array(SAV, ref_len),
        pad_array(CAV, ref_len)
    ]
    labels = ["Tsource (°C)", "GR (nm/s)", "conc_all (cm-3)", "conc_CV (cm-3)", "conc_SV (cm-3)", "conc_SAV (cm-3)", "conc_CAV (cm-3)"]
    np.savetxt(
        'results.txt',
        np.column_stack(data),
        delimiter="\t",
        fmt="%.5e",
        header="# " + "\t".join(labels),
        comments="# Tseed={}°C, randseed={}\n".format(Tseed, randseed)
    )
    print("✅ File 'results.txt' salvato con eventuali NaN per dati mancanti.")
except Exception as e:
    print(f"[WARNING] 'results.txt' non salvato: {e}")

# SE SERVISSE RIPLOTTARE QUALCOSA...
# Tsource, gr_KMC_nms, vac_tot, CV, SV, SAV, CAV = np.loadtxt('results.txt', unpack=True)