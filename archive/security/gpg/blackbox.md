# Use GPG and Blackbox to encrypt files

[Blackbox](https://github.com/StackExchange/blackbox) is a nice way to safely
store secrets needed for deploying applications in a publicly accessible
version control system (like GitHub). The short of it is that it leverages [GPG
encryption](https://www.gnupg.org/) to sign and encrypt files with a given set of keys that can then be
used to decrypt the files when needed on a remote host. After it is set up and your
key is added to the keychain, you shouldn't really need to touch much of
anything except when you want to modify the files that are being encrypted.

## Initial setup

If you already have a GPG key, you can skip ahead to [installing blackbox](#install-blackbox); if you already have blackbox configured on your machine, go ahead and skip to [project setup](#project-setup).

### Create a GPG key

For Mac OS X users, [this
guide should help you install GPG](http://notes.jerzygangi.com/the-best-pgp-tutorial-for-mac-os-x-ever/)
using the program GPG Suite. You can also use [this guide](http://keyring.debian.org/creating-key.html)
to install GPG on the command line.

If at any point in this process you're prompted to create entropy so that the random
number generator can generate a lot of random bytes, a great command to run is:

```bash
sudo dd if=/dev/sda of=/dev/null
```

This just tells your computer to create a copy your main disk and place it
into the void, generating a ton of entropy in the process.

Here's what the output should look like using the command line:

```bash
gpg --gen-key
gpg (GnuPG) 1.4.18; Copyright (C) 2014 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

gpg: keyring `./secring.gpg' created
gpg: keyring `./pubring.gpg' created
Please select what kind of key you want:
   (1) RSA and RSA (default)
   (2) DSA and Elgamal
   (3) DSA (sign only)
   (4) RSA (sign only)
Your selection? 1
RSA keys may be between 1024 and 4096 bits long.
What keysize do you want? (2048) 4096
Requested keysize is 4096 bits
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0)
Key does not expire at all
Is this correct? (y/N) y

You need a user ID to identify your key; the software constructs the user ID
from the Real Name, Comment and Email Address in this form:
    "Heinrich Heine (Der Dichter) <heinrichh@duesseldorf.de>"
Real name: Example key
Email address: example@example.com
Comment:
You selected this USER-ID:
    "Example key <example@example.com>"

Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? O
You need a Passphrase to protect your secret key.

We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.
.......+++++
.....................+++++
......................+++++
+++++
gpg: ./trustdb.gpg: trustdb created
gpg: key B5C7EFB7 marked as ultimately trusted
public and secret key created and signed.

gpg: checking the trustdb
gpg: 3 marginal(s) needed, 1 complete(s) needed, PGP trust model
gpg: depth: 0  valid:   1  signed:   0  trust: 0-, 0q, 0n, 0m, 0f, 1u
pub   4096R/B5C7EFB7 2016-03-07
      Key fingerprint = 2C75 37E3 044A BE39 6C12  A57F E888 D74A B5C7 EFB7
uid                  Example key <example@example.com>
sub   4096R/5EC12084 2016-03-07
```

Congratulations! You now have a GPG key.

### Install Blackbox

MacOS users can install Blackbox with Homebrew:

``` bash
brew install blackbox
```

Blackbox can also be installed easily from source:

```bash
# Grab the Blackbox repo with git
git clone https://github.com/StackExchange/blackbox

# Build Blackbox
cd blackbox
sudo make symlinks-install
```

Blackbox has [detailed installation
instructions](https://github.com/StackExchange/blackbox#installation-instructions)
if you need to troubleshoot the installation.

## Project setup

### Initialize Blackbox

The first person to start a project gets the honor of initializing it and being
the first person in the keyring that can decrypt files and add others to the
keyring.

#### GPG history break

Before you initialize Blackbox, it's important to note that there are some
differences between how GPG 1.x and GPG 2.x create encryption artifacts. This
will matter if you're sharing files with someone using a different version: If you
initialize Blackbox using GPG 2.x locally, users of GPG 1.x  will fail to decrypt
your files with an error like this:

```
gpg: [don't know]: invalid packet (ctb=00)
gpg: key export failed: invalid packet
```

So, make note of your GPG version now.

```
gpg --version
gpg (GnuPG) 2.2.16
...
```

#### Back to the tutorial...

Once a project is setup to use git, you can do that like so:

``` bash
cd path/to/project
blackbox_initialize
```

That will generate some output that looks like this:

```
Enable blackbox for this git repo? (yes/no) yes
VCS_TYPE: git


NEXT STEP: You need to manually check these in:
      git commit -m'INITIALIZE BLACKBOX' keyrings /home/eric/code/blackbox-test/.gitignore
```

Do as it says and commit that change. Next, add yourself as an admin to the project:

```
# Replace my email address with whatever the email address was that you used to
# create your GPG key
blackbox_addadmin eric@e-vz.com
```

The output from that command should look something like:

```
gpg: keyring `/home/eric/code/blackbox-test/keyrings/live/secring.gpg' created
gpg: keyring `/home/eric/code/blackbox-test/keyrings/live/pubring.gpg' created
gpg: /home/eric/code/blackbox-test/keyrings/live/trustdb.gpg: trustdb created
gpg: key 25E7098A: public key "Eric van Zanten <eric@e-vz.com>" imported
gpg: Total number processed: 1
gpg:               imported: 1  (RSA: 1)


NEXT STEP: You need to manually check these in:
      git commit -m'NEW ADMIN: eric@e-vz.com' keyrings/live/pubring.gpg keyrings/live/trustdb.gpg keyrings/live/blackbox-admins.txt

```

Again, go ahead and commit those changes and push the changes to GitHub. At
this point, you might want to add a file to encrypt. You can do that like so:

``` bash
blackbox_register_new_file Decrypt-me-if-you-can.md
```

That should generate output that looks something like:

```
========== PLAINFILE Decrypt-me-if-you-can.md
========== ENCRYPTED Decrypt-me-if-you-can.md.gpg
========== Importing keychain: START
gpg: Total number processed: 1
gpg:              unchanged: 1
========== Importing keychain: DONE
========== Encrypting: Decrypt-me-if-you-can.md
========== Encrypting: DONE
========== Adding file to list.
========== CREATED: Decrypt-me-if-you-can.md.gpg
========== UPDATING REPO:
NOTE: "already tracked!" messages are safe to ignore.
[master eb681eb] registered in blackbox: Decrypt-me-if-you-can.md
 2 files changed, 1 insertion(+)
 create mode 100644 Decrypt-me-if-you-can.md.gpg
========== UPDATING VCS: DONE
Local repo updated.  Please push when ready.
    git push
```

You can then push that file to GitHub knowing that only you have the power to
unlock it's secrets.

### Add another user

However, most of the time we'll want to be able to collaborate on things, even
files that have encrypted secrets. To indoctrinate another user into the
project, make sure you've [imported their public
key](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/4/html/Step_by_Step_Guide/s1-gnupg-import.html)
and run the following code:

``` bash
git clone git@github.com:datamade/blackbox-test.git
cd blackbox-test

# Replace fake email address with the email address that they registered with
# their GPG key
blackbox_addadmin user@domain.com
```

This will generate the same output as before. Before committing the changes, you'll
need to re-encrypt the existing files using the updated keyring in order to allow
the new admin to decrypt them:

``` bash
# Re-encrypt the files
blackbox_update_all_files

# Commit and push the files
git commit -a
git push origin master
```

Now, just to test things out, have the user who was just added pull the changes
and see if they can decrypt the files:

``` bash
cd path/to/project
git pull origin master
blackbox_cat /path/to/encrypted/file
```

That should just `cat` the file out to your terminal. If that worked, you
should also be able to actually edit, add and remove files, too.

### Modifying files

This will launch whatever your default editor is (defined by the $EDITOR
environmental variable), allow you to edit the file and, when you save and
close it, re-encrypt the file all in one go.

``` bash
blackbox_edit /path/to/encrypted/file
```

If that didn't work or it launched some editor that you're not used to, you can
also take in one step at a time like so:

``` bash
blackbox_edit_start /path/to/encrypted/file

# Now open the decrypted file in whatever you want, save it and close it.

blackbox_edit_end /path/to/encrypted/file

```

To add a file, use `blackbox_register_new_file` and to remove a file use
`blackbox_deregister_file`. More commands and details about how to use Blackbox
can be found in their [GitHub repo](https://github.com/StackExchange/blackbox)
