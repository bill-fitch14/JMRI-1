package jmri.jmrit.vsdecoder;

import jmri.*;
import jmri.util.JUnitUtil;
import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

/**
 *
 * @author Paul Bender Copyright (C) 2017
 */
public class DieselSoundTest {

    @Test
    public void testCTor() {
        DieselSound t = new DieselSound("test");
        Assert.assertNotNull("exists",t);
    
        // this created an audio manager, clean that up
        InstanceManager.getDefault(jmri.AudioManager.class).cleanup();
    }

    @Before
    public void setUp() {
        JUnitUtil.setUp();
    }

    @After
    public void tearDown() {
        JUnitUtil.tearDown();
    }

    // private final static Logger log = LoggerFactory.getLogger(DieselSoundTest.class);

}
