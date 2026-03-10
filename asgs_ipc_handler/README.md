# ASGS Server
A light server process to give ASGS the ability to handle IPC for the purpose of building building ASGS APIs.
 
To run:
* Edit `ASGS_HOME` in `asgs_server.sh`
1. Start ASGS as a server:
   - `./asgs_server.sh &`
2. Connect to the generated pipes using `main.sh` or manually.
3. You`re G2G. You can connect and disconnect at will.
4. To close send `exit` through `pipein` or run `kill pid` on the asgs pid that was given at start.

## Infrastructure
ASGS demands to be a terminal application. This results in more traditional ways of communicating
with it as a sub/parallel process difficult. To solve this the linux command `script` is used. 
`script` creates a psuedo-terminal to trick ASGS into thinking it is working normally. During creation
the pty has its std{in,out} redirected through $server_meta_dir/pipe{in,out}. Additionally, a second process
is spawned, `tail -f /dev/null > pipein &`. This is done so that pipein is always open. This non blocking
write operation essentially supresses the kernal from closing the pipe, which would cause `script` to crash. 

At initiation, `asgs_server.sh` will create a dir `~/.asgsh`. The pipes and a file containing the pids for 
the server and pipe tender. `asgs_server.sh` `wait`s on `script`. When `script` completes, for any reason, 
the tender process is killed and `~/.asgsh` is removed.

## Manual Connection
To connect manually, have your process connect to the pipes in this order:
1. open pipeout for reading
2. Open pipein for writing
Then, simply send commands over the pipes like it was a normal `asgsh` session. This can be done manually
or by having a function like:
```python
def list_adcirc(pipein,pipeout):
    pipein.write(b"list adcirc\n")
    adcircs=pipeout.readline().strip().split()
    pipeout.readline() # Clears the command prompt out of pipeout
    return adcircs
``` 
