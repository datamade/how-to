# tmux: some considerations, some best practices

tmux provides a way to multiply terminal windows and run processes in the background. Often on DataMade servers, we need to execute commands that require several hours to complete. tmux offers a solution for doing so, without the worries and headaches that come with losing connectivity mid-process. 

No problem, right? Almost.

Multiple datamakers might log into the same server and open tmux sessions. Lingering sessions can persist and confuse others of their usefulness. The below outlines some best practices for using tmux on DataMade servers.

* **Use tmux as the ubuntu user (if needed, switch to datamade user within the tmux session).**

* **Create named sessions. Use your name plus a description of the process.**

  ```bash
  tmux new -s <yourname-process>
  ``` 

* **Exit the session with care (i.e., be cautious about killing the session with ctrl +  d)**

  ```bash
  # Detach from the session
  ctrl + b
  d
  ```

* **Terminate the session, after your process finishes. You can do this several ways - just be sure it gets done!**

  ```bash
  # Is the process done?
  tmux a -t <session name>
  # If so, kill it
  ctrl + d
  # Or detach from the session, and kill it
  tmux kill-session -t <session name>
  ```

----

Looking for a cheatsheet? [Read more about tmux shortcuts here.](https://gist.github.com/MohamedAlaa/2961058)