FROM archlinux/base

RUN pacman -Syu --noconfirm

WORKDIR /root/

RUN echo "echo ""; echo "Welcome in pluto-GSI container [https://github.com/aszadzinski/dockerfiles/tree/master/physics-simulations/pluto-GSI]"; echo "You can find libPluto.so in pluto_v6.01/build/"; echo ""; echo "Type:"; echo "  sh init.sh"; echo "to execute Public/run.sh."; echo "" " >> .bashrc
RUN echo "echo "Opening Public/run.sh file..."; echo ""; sh /root/Public/run.sh; echo ""; echo "Done."" >>dd init.sh 

#ENTRYPOINT ["sh","init.sh"]
CMD sh init.sh
