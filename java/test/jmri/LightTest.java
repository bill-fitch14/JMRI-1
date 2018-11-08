package jmri;

import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;
import java.beans.PropertyVetoException;
import java.util.ArrayList;
import java.util.Set;
import jmri.implementation.LightControl;
import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;
import org.junit.Assert;

/**
 * Tests for the Light class
 *
 * @author	Bob Jacobsen Copyright (C) 2008, 2010
 */
public class LightTest extends TestCase {

    @SuppressWarnings("all")
    public void testStateConstants() {
        Assert.assertTrue("On and Off differ", (Light.ON & Light.OFF) == 0);
        Assert.assertTrue("On and Unknown differ", (Light.ON & Light.UNKNOWN) == 0);
        Assert.assertTrue("Off and Unknown differ", (Light.OFF & Light.UNKNOWN) == 0);
        Assert.assertTrue("On and Inconsistent differ", (Light.ON & Light.INCONSISTENT) == 0);
        Assert.assertTrue("Off and Inconsistent differ", (Light.OFF & Light.INCONSISTENT) == 0);
    }

    @SuppressWarnings("all")
    public void testTransitionConstants() {
        Assert.assertTrue("On and INTERMEDIATE are bits", (Light.ON & Light.INTERMEDIATE) == 0);

        Assert.assertTrue("TRANSITIONINGTOFULLON overlap", (Light.TRANSITIONINGTOFULLON & Light.TRANSITIONING) != 0);
        Assert.assertTrue("TRANSITIONINGHIGHER overlap", (Light.TRANSITIONINGHIGHER & Light.TRANSITIONING) != 0);
        Assert.assertTrue("TRANSITIONINGLOWER overlap", (Light.TRANSITIONINGLOWER & Light.TRANSITIONING) != 0);
        Assert.assertTrue("TRANSITIONINGTOFULLOFF overlap", (Light.TRANSITIONINGTOFULLOFF & Light.TRANSITIONING) != 0);
    }

    public void testLight() {
        Light light = new MyLight();
        light.setState(Light.ON);
        Assert.assertTrue("Light is ON", light.getState() == Light.ON);
        light.setState(Light.OFF);
        Assert.assertTrue("Light is ON", light.getState() == Light.OFF);
        light.setCommandedState(Light.ON);
        Assert.assertTrue("Light is ON", light.getState() == Light.ON);
        light.setCommandedState(Light.OFF);
        Assert.assertTrue("Light is ON", light.getState() == Light.OFF);
        light.setState(Light.ON);
        Assert.assertTrue("Light is ON", light.getCommandedState() == Light.ON);
        light.setState(Light.OFF);
        Assert.assertTrue("Light is ON", light.getCommandedState() == Light.OFF);
        light.setState(Light.ON);
        Assert.assertTrue("Light is ON", light.getKnownState() == Light.ON);
        light.setState(Light.OFF);
        Assert.assertTrue("Light is ON", light.getKnownState() == Light.OFF);
    }

    // from here down is testing infrastructure
    public LightTest(String s) {
        super(s);
    }

    // Main entry point
    static public void main(String[] args) {
        String[] testCaseName = {LightTest.class.getName()};
        junit.textui.TestRunner.main(testCaseName);
    }

    // test suite from all defined tests
    public static Test suite() {
        TestSuite suite = new TestSuite(LightTest.class);
        return suite;
    }

    
    
    private class MyLight implements Light {
        
        private int _state = NamedBean.UNKNOWN;

        @Override
        public void setState(int newState) {
            _state = newState;
        }

        @Override
        public int getState() {
            return _state;
        }

        @Override
        public boolean isIntensityVariable() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public void setTargetIntensity(double intensity) {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public double getCurrentIntensity() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public double getTargetIntensity() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public void setMaxIntensity(double intensity) {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public double getMaxIntensity() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public void setMinIntensity(double intensity) {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public double getMinIntensity() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public boolean isTransitionAvailable() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public void setTransitionTime(double minutes) {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public double getTransitionTime() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public boolean isTransitioning() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public void clearLightControls() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public void addLightControl(LightControl c) {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public ArrayList<LightControl> getLightControlList() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public void setEnabled(boolean state) {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public boolean getEnabled() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public void activateLight() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public void deactivateLight() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public String getUserName() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public void setUserName(String s) throws BadUserNameException {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public String getSystemName() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public String getDisplayName() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public String getFullyFormattedDisplayName() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public void addPropertyChangeListener(PropertyChangeListener l, String name, String listenerRef) {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public void addPropertyChangeListener(PropertyChangeListener l) {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public void removePropertyChangeListener(PropertyChangeListener l) {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public void updateListenerRef(PropertyChangeListener l, String newName) {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public void vetoableChange(PropertyChangeEvent evt) throws PropertyVetoException {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public String getListenerRef(PropertyChangeListener l) {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public ArrayList<String> getListenerRefs() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public int getNumPropertyChangeListeners() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public PropertyChangeListener[] getPropertyChangeListenersByReference(String name) {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public void dispose() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public String describeState(int state) {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public String getComment() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public void setComment(String comment) {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public void setProperty(String key, Object value) {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public Object getProperty(String key) {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public void removeProperty(String key) {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public Set<String> getPropertyKeys() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public String getBeanType() {
            throw new UnsupportedOperationException("Not supported.");
        }

        @Override
        public int compareSystemNameSuffix(String suffix1, String suffix2, NamedBean n2) {
            throw new UnsupportedOperationException("Not supported.");
        }
        
    }
    
}
