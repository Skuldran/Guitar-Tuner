def tone2freq(tone):
    
    tones = ["A", "A#", "B", "C", "C#", "D", "D#", "E", \
             "F", "F#", "G", "G#"];
    
    try:
        octave = int(tone[-1]);
        note = tone[:-1];
        
        i = tones.index(note);
        if i>4:
            octave -= 1
        
        num = (octave-4)*12+i;    
        K = 2**(1/float(12)) #12th root of 2
    
        return 440*(K**(num))
        
    except:
        raise Exception("Invalid note format.")
            
            
    


print(tone2freq("G4"))