First, I plan to finish the Prolblem, and I need prompt to talk with AI to finish the game design. So I used `plan` to ask Claude Opus 4.5: `Following the illustrations in #file:Guide.md, I first need to develop a game named Pac-Man(Valentine's Special), which corresponds to the Problem 2. For this game, the user can play this game on on a browser by opening html. I want to use Python to code. Please give me a detailed prompt on the instruction of this task.`

Then, I request him to `saved this prompt into a markdown file, and then Please do the task and write the code.`

The game runs normally, but there are some issues. Ghosts appear at the start of the game, but instead of chasing Pac-Man, they go to the same spot one by one and then stop.

The game runs normally, but the issues still exist. Ghosts appear at the start of the game, but instead of chasing Pac-Man, they go to the same spot one by one and then stop. The ghost is expected to move and chase Pac-Man rather than staying in the same plance.




After that, I moved to the Problem 1. Here is my propmt: `Following the illustrations in #file:Guide.md, I need Create a homepage for a website for my coding blog. The website should be hosted on [GitHub Pages](https://pages.github.com/). You can design the homepage by yourself in any proper style you like. You may need to make the design expandable to add more content from our future assignments. The link to the homepage should be added to the README.md of your homework repository so that anyone can access the homepage and the following two webpages from the Internet using this link. And we already develop the game:  Pac_Man, saved in the Pac_Man folder`

The Coding Blog was built successfully, but I still face some issues. That is, the game can't be accessed through index.html. Here is my prompy `I have Build the Pac-Man game using 'pygbag --build main.py', and generated the file saved in Pac_Man/build folder. And following the instructions, I copy the contents in Pac_Man/build/web and paste them in coding_blog/games/pacman_build. But I faced issues to open the game after clicking index.html, and it returned Loading, please wait, but no more changes.`


It shows loding first, and then change to ready to start, please click/touch page, but after clicking, I still fail to play the game. 

The problem persists. After clicking the "Ready to start, please click/touch the page" message, the page turns gray. Additionally, I cannot load the game interface from 'Pac_Man/build/web/index.html'.

Change to Java Script.
How to open the coding blod website and run the pac mac game

I can open the website but fail to start the game as the game window in the page is completely black, even though I have pressed start button

I can play the game through 'python main.py' in the folder Pac_Man', but I fail to play the game in the html you show me. And the game window is always black. Could you solve this issue

I can start the game now, but the ghosts seem to have some problems moving. When I move Pac-Man, the ghosts can't catch me; they don't seem to understand the structure of the obstacles in the maze, and even when they can move, they can't leave the area where they appear.

The movement of ghost still have several issues. After my Pac-Man meet with the ghost and die, some ghosts will stop chaing Pac-Man. I remember in the original Pac_Man game, this issue didn't appear. Could you check why it happens and solve it.

similar issues as before. When I move Pac-Man, the ghosts can't catch me; they don't seem to understand the structure of the obstacles in the maze, and even when they can move, they can't leave the area where they appear. And when they leave the birth region and begin to chase me, some of them will stop chasing me. Also, the game before we build website seems work well. That is to say, these issues not exist when running 'Pac_Man % python main.py'. 


Everything is great, but the ghost is much faster than Pac-Man, could make it a little slower?

Finally, I moved to the Problem 3. Here is my prompt `In this part, I plan to build an auto-updating arXiv paper feed in my website. I plan to break the task into agent-friendly steps, prompt the agent effectively, and wire everything together, could you show me the prompt that can help Copilot CLI to code. Here are several requirement: Add a new page to your website that displays the latest arXiv papers. The page must include: 1. **Paper Listing**: The latest arXiv papers matching keywords of your choice. Design the layout as you see fit. 2. **Paper Details**: Each entry must show the paper title, authors, abstract, and a direct link to the PDF. 3. **Auto-Update**: The paper list must refresh automatically every midnight via a GitHub Actions workflow. 4. **Homepage Link**: A link to this page must appear on your homepage from Problem 1. 5. **Page Design**: Style the page in any way you think readers would appreciate. And detailed illustations can be found in #Guide.md`

Nice, there are something I want to futher check: (1) could I change the keywords, and then the paper shown will be changed correspondingly. The keywords now seems fixed; (2)