# cs618-final-project

# random immunization
![degree](random.gif)
![degree](random.png)

# highest-degree immunization
![degree](degree.gif)
![degree](degree.png)

# Some kind of epidemic simulator
- Description
    - Graph `G` that consists of nodes `N`
        - Graphs generated with https://networkx.org/documentation/stable/reference/generators.html
    - Set of agents `A`
        - Possible actions
            - Move - move to an adjacent node
            - Stay - stay at the current node
            - Return - return to the previous node
                - Or return to starting node? This makes sense: agent will travel around, then go back to where they started (home?)
    - Interaction model
        - At every timestep `t`:
            - Every agent performs `1` action
    - Transmission model
        - Get set of nodes that contain infected agents
        - If node also contains susceptible agents:
          - Let `tp` be the probability of transmission
          - Let `ni` be the number of infected agents at the node
          - Susceptible agents have a `tp * ni` probability of infection
    - Immunization models
        - Random
            - `n` nodes every timestep?
            - `n` nodes all at once?
        - Immunize node(s) with highest degree
            - All at once?
            - `n` of them every timestep?
        - Immunize most frequently traveled nodes
            - Calculate frequency every timestep
            - `n` of them every timestep?
        - When to immunize?
            - After certain percentage of population infected?
            - After certain number of timesteps?
        - Should vaccines be a limited resource?
    - Other
        - Can try to enforce "social distancing" by lowering agent travel probability during epidemic?
        - Can have a percentage of population ignore this
        - Can have a percentage of population be "anti-vax"

# What to look at?
- social distancing
    - show effects of social distancing with percentage of population participating
    - compare graphs
    - find where social distancing breaks down when enough agents do not participate
- immunization
    - show effects of immunization with different strategies
    - compare graphs
    - random strategy
    - highest degree node strategy
    - most frequently traveled strategy
    - find where immunization breaks down when enough agents do not participate?

# Requirements
- Python 3.8.1
```sh
# Name                    Version                   Build  Channel
_libgcc_mutex             0.1                        main  
attrs                     21.2.0             pyhd3eb1b0_0  
backcall                  0.2.0              pyhd3eb1b0_0  
blas                      1.0                         mkl  
ca-certificates           2021.4.13            h06a4308_1  
certifi                   2020.12.5        py38h06a4308_0  
cycler                    0.10.0                   py38_0  
dbus                      1.13.18              hb2f20db_0  
decorator                 4.4.2              pyhd3eb1b0_0  
expat                     2.3.0                h2531618_2  
fontconfig                2.13.1               h6c09931_0  
freetype                  2.10.4               h5ab3b9f_0  
glib                      2.68.1               h36276a3_0  
gst-plugins-base          1.14.0               h8213a91_2  
gstreamer                 1.14.0               h28cd5cc_2  
icu                       58.2                 he6710b0_3  
imageio                   2.9.0              pyhd3eb1b0_0  
importlib-metadata        3.10.0           py38h06a4308_0  
importlib_metadata        3.10.0               hd3eb1b0_0  
intel-openmp              2021.2.0           h06a4308_610  
ipykernel                 5.1.4            py38h39e3cac_0  
ipython                   7.22.0           py38hb070fc8_0  
ipython_genutils          0.2.0              pyhd3eb1b0_1  
jedi                      0.16.0                   py38_1  
joblib                    1.0.1              pyhd3eb1b0_0  
jpeg                      9b                   h024ee3a_2  
jsonschema                3.2.0                      py_2  
jupyter_client            6.1.12             pyhd3eb1b0_0  
jupyter_core              4.7.1            py38h06a4308_0  
kiwisolver                1.3.1            py38h2531618_0  
lcms2                     2.12                 h3be6417_0  
ld_impl_linux-64          2.33.1               h53a641e_7  
libedit                   3.1.20210216         h27cfd23_1  
libffi                    3.3                  he6710b0_2  
libgcc-ng                 9.1.0                hdf63c60_0  
libgfortran-ng            7.3.0                hdf63c60_0  
libpng                    1.6.37               hbc83047_0  
libsodium                 1.0.18               h7b6447c_0  
libstdcxx-ng              9.1.0                hdf63c60_0  
libtiff                   4.1.0                h2733197_1  
libuuid                   1.0.3                h1bed415_2  
libxcb                    1.14                 h7b6447c_0  
libxml2                   2.9.10               hb55368b_3  
lz4-c                     1.9.3                h2531618_0  
matplotlib                3.1.3                    py38_0  
matplotlib-base           3.1.3            py38hef1b27d_0  
mkl                       2021.2.0           h06a4308_296  
mkl-service               2.3.0            py38h27cfd23_1  
mkl_fft                   1.3.0            py38h42c9631_2  
mkl_random                1.2.1            py38ha9443f7_2  
nbformat                  5.0.4                      py_0  
ncurses                   6.2                  he6710b0_1  
networkx                  2.5.1              pyhd3eb1b0_0  
numpy                     1.20.2           py38h2d18471_0  
numpy-base                1.20.2           py38hfae3a4d_0  
olefile                   0.46                       py_0  
openssl                   1.1.1k               h27cfd23_0  
pandas                    1.0.3            py38h0573a6f_0  
parso                     0.8.2              pyhd3eb1b0_0  
pcre                      8.44                 he6710b0_0  
pexpect                   4.8.0              pyhd3eb1b0_3  
pickleshare               0.7.5           pyhd3eb1b0_1003  
pillow                    8.2.0            py38he98fc37_0  
pip                       21.0.1           py38h06a4308_0  
plotly                    4.5.2                      py_0  
prompt-toolkit            3.0.17             pyh06a4308_0  
ptyprocess                0.7.0              pyhd3eb1b0_2  
pygments                  2.8.1              pyhd3eb1b0_0  
pyparsing                 2.4.7              pyhd3eb1b0_0  
pyqt                      5.9.2            py38h05f1152_4  
pyrsistent                0.17.3           py38h7b6447c_0  
python                    3.8.1                h0371630_1  
python-dateutil           2.8.1              pyhd3eb1b0_0  
pytz                      2021.1             pyhd3eb1b0_0  
pyzmq                     20.0.0           py38h2531618_1  
qt                        5.9.7                h5867ecd_1  
readline                  7.0                  h7b6447c_5  
retrying                  1.3.3                      py_2  
scikit-learn              0.24.1           py38ha9443f7_0  
scipy                     1.6.2            py38had2a1c9_1  
seaborn                   0.10.0                     py_0  
setuptools                52.0.0           py38h06a4308_0  
sip                       4.19.13          py38he6710b0_0  
six                       1.15.0           py38h06a4308_0  
sqlite                    3.31.1               h7b6447c_0  
threadpoolctl             2.1.0              pyh5ca1d4c_0  
tk                        8.6.10               hbc83047_0  
tornado                   6.1              py38h27cfd23_0  
tqdm                      4.59.0             pyhd3eb1b0_1  
traitlets                 5.0.5              pyhd3eb1b0_0  
wcwidth                   0.2.5                      py_0  
wheel                     0.36.2             pyhd3eb1b0_0  
xz                        5.2.5                h7b6447c_0  
zeromq                    4.3.4                h2531618_0  
zipp                      3.4.1              pyhd3eb1b0_0  
zlib                      1.2.11               h7b6447c_3  
zstd                      1.4.9                haebb681_0
```