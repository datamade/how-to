# How to move a gpg key between servers

Sometimes, you need to move a gpg key from one server to another. 

But why?

Let's say, you prepare a site to deploy to staging. You create a gpg key on your local machine, and you export it to the staging server. For the sake of good house keeping, you then remove the key from your local machine. Days, weeks, months elapse - and, now, you (or someone else) needs to deploy the app to production *on a different server*. You need the gpg key to do so, and the key only lives in one place: the staging server. 

Another example. Let's say, you need to migrate an application from its current server to a new server: for this, the gpg key of the application must be included on the new server's keyring. Again, the gpg key only resides on its current server. 

If these situations sound familiar, then learn how to seamlessly and securely move a gpg key to from one destination to another. 

#### 1. On your local machine, add your private SSH key (i.e., id_rsa) to the ssh-agent.

```
# local machine
ssh-add ~/.ssh/id_rsa
```

#### 2. Shell into the "old" server, and in doing so, forward the authentication credentials to this server.

```
# "old" server (ubuntu user)
ssh -A ubuntu@oldserver.datamade.us
```

#### 3. Switch to the datamade user, and view secret keys.

```
# "old" server (datamade user)
sudo su - datamade
gpg --list-secret-keys
```

```
# Sample results of --list-secret-keys
/home/datamade/.gnupg/secring.gpg
---------------------------------
sec   4096R/6129A997 2017-03-17
uid                  la-metro-staging <datamade@lametro.datamade.us>
ssb   4096R/42C4F8BB 2017-03-17
ssb   4096R/92F1611F 2017-03-17
```

#### 4. Put the needed key into a readable file. 

You can call this file whatever you want, e.g., "pubkey.txt". However, the email address should correspond to the `uid` from `--list-secret-keys`, since it's the one in `keyrings/live/blackbox-admins.txt` of your application.

```
# "old" server (datamade user)
gpg --export-secret-key datamade@lametro.datamade.us > pubkey.txt
```

#### 5. Switch back to Ubuntu user (to avoid permission errors when transferring the key via SCP). Then, move the key, and change its ownership.

```
# "old" server (ubuntu user)
sudo mv /home/datamade/pubkey.txt .
sudo chown ubuntu.ubuntu pubkey.txt
```

#### 6. Still on the old server, as the Ubuntu user, [securely transfer the key using SCP](https://en.wikipedia.org/wiki/Secure_copy) to the specified "new" server.

```
# "old" server (ubuntu user)
scp pubkey.txt ubuntu@newserver.datamade.us:/home/ubuntu
```

#### 7. On your local machine, shell into the "new" server.

```
# local machine
ssh ubuntu@newserver.datamade.us
```

#### 8. Move the key, and change its ownership.

```
# "new" server (ubuntu user)
sudo mv pubkey.txt /home/datamade/
sudo chown datamade.datamade /home/datamade/pubkey.txt
```

####  9. Change to the DataMade user. Import the key, and check your work: the `uid` of the key you moved should appear in list of secret keys.

```
# "new" server (datamade user)
sudo su - datamade
gpg --import pubkey.txt
gpg --list-secret-keys
```