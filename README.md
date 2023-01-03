# ToonSnapshotBot

```commandline


/ : command or subcommand


/render
    /toon
        - dnastring: optional>None
            > dictates if randomDNA will be used or not; None=randomDNA
        - muzzle: optional>default
            > autocomplete
        - eyes: optional>default
            > autocomplete
        - nametag: optional>True
            > if False, code should not consider setName
        - name: optional>None
            > if None, generate random name
        - pose: optional>random ** random may include more if over limit?
            > autocomplete: neutral, pose names
        - cheesyeffect: optional>None
        - picture_type: optional>fullbody
            > autocomplete: toptoons, fullbody, headshot
        
    /npc
        - npcid: optional>None
            > if not None, take in a string and convert it to its npc id equivalent
            > have an autocomplete list for notable NPC toons
            > maybe have a check to see if input is just ints to skip name check
        - nametag: optional>true
        - pose: optional>random
        - info: optional>False
            > print extra info about the npc, including the shop name (street and pg too), if toon is random dna'd, npc type, etc
        
    /doodle
    /cog
    /custom
        - selection menu using discord.ui.View
        - possibly as subcommands too? `/custom toon head` can return client sided preview pictures
        - ephermal / client sided input
        - once a cog/toon/doodle is selected and a preset is generated, 
        - use the same message, maybe arrows to go back and forth?
        - use reference images for showing options, can we do that with local image storage
        - variation options can always have a "random" tag at the end
        - should be fun to have an absolute true random generation
        ** do not know how this will work with paralell unless we can GET A RENDER QUEUE
        ** idk how im gonna generate clothing since there's so many, accessories too
        Choose Between:
        | Cog
        | Toon
            | Species
                > possible to include image of all species?
                | cat, dog, etc., random
            | Gender
                > possibly buttons instead of a dropdown
                | male, female, random
            | Head Type
                > possible to show a picture of all the different head styles?
            | Head Color
                > show color list
            | Eyes
                | normal, normal closed, angry, etc.
            | Muzzle Type
                | yeah
            | Torso Type
                > ditto, should we pre-render a template toon with applied changes? (ephermal)
                > image should keep editing itself until user is complete
            | Torso Color
            | Leg Type
                > ditto
            | Leg Color
            | Pose
                > buttons
                | Preset
                    > preset ids in a friendly name
                | Custom
                    | Animation
                        > show text list of all possible toon anims
                    | Frame
                        > get it with anim entered
                    | Offset: optional>(0, 0, 0, 0, 0, 0, 0, 0, 0)
                        > xyz hpr SxSySz
                        > i dont think im gonna do this anytime soon lol
            | Cheesy Effect
            | Name
        | Doodle 

```