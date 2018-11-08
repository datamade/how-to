# How to move a gpg key between servers

Sometimes, you need to move a gpg key from one server to another. 

But why?

Let's say, you prepare a site to deploy to staging. You create a gpg key on your local machine, and you export it to the staging server. For the sake of good housing keeping, you then remove the key from your local machine. Days, weeks, months elapse - and, now, you (or someone else) needs to deploy the app to production *on a different server*.

Or, you need to migrate an application from its current server to a new server: this requires the gpg key of the application to be included on the server keyring. 

1. On your local machine, add your private SSH key (i.e., id_rsa) to the ssh-agent.

```
ssh-add ~/.ssh/id_rsa
```

2. Shell into the "old" server, and in doing so, forward the authentication credentials to the server.

```
ssh -A ubuntu@oldserver.datamade.us
```

3. Switch to the datamade user, and view secret keys. Translate the needed key into a readable file, which you can call whatever you want, e.g., "pubkey.txt". (The email address should correspond to the one in the keyrings/live/blackbox-admins.txt)

```
sudo su - datamade
gpg --list-secret-keys
gpg --export-secret-key datamade@lametro.datamade.us > pubkey.txt
```

4. Switch back to Ubuntu user, move the key, and change its ownership.

```
sudo mv /home/datamade/pubkey.txt .
sudo chown ubuntu.ubuntu pubkey.txt
```

5. SCP the key to the specified production server, shell into that server, and change to the DataMade user.

```
scp pubkey.txt ubuntu@newserver.datamade.us:/home/ubuntu
ssh ubuntu@newserver.datamade.us
sudo su - datamade
```

6. Move the key, and change its ownership.

```
sudo mv pubkey.txt /home/datamade/
sudo chown datamade.datamade /home/datamade/pubkey.txt
```

7. Import the key, and check your work.

```
gpg --import pubkey.txt
gpg --list-secret-keys
```