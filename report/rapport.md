# Accelerometer-based measurement to quantify muscle fatigue

**Authors :** Mahoua KONE, Lucie BONNOT, Loubna EL FARESSI, Bomane PEHE 
**Date :** November 10, 2025  
**Supervisor :** Denis MOTTET

---

## 1. Introduction


### Muscular Fatigue and Accelerometry Analysis

Muscular fatigue is characterized by a progressive decline in a muscle’s ability to generate force, manifesting as alterations in movement execution, reduced range of motion, or decreased movement regularity. Although physiological tools such as electromyography, heart rate monitoring, or blood lactate assessment can be used to quantify fatigue, these methods are often costly, invasive, or difficult to implement in real-world conditions.

Inertial sensors, particularly accelerometers, offer a simple, portable, and non-invasive alternative for analyzing movement dynamics. By measuring acceleration along three axes, they provide a quantitative estimation of movement intensity, notably through the acceleration norm.

---

### Objective of the Study

In this project, we examined the evolution of acceleration signals during a jump-rope exercise. The goal was to determine whether the placement of the sensor influences the ability to detect muscular fatigue throughout the task. Two locations were tested within the same session:

- **Right wrist** — primarily involved in rope rotation  
- **Right ankle** — directly associated with take-off and landing phases
---

### Working Hypothesis

Our general hypothesis is that the dynamics of the acceleration signal depend on sensor location, as the wrist and ankle are subjected to different biomechanical constraints.

More specifically, we assumed that:

The ankle-mounted sensor would be more sensitive to fatigue-related changes, as it captures variations in propulsion, stability, and impact forces during jumps.

The wrist-mounted sensor would mainly reflect rope rotation, which is expected to be less affected by lower-limb muscular fatigue.

---

### Data Processing and Analysis

To test this hypothesis:

1. The acceleration signal was analyzed over the full duration of the exercise.
2. The signal was segmented into **normalized time intervals**, allowing us to observe changes in movement intensity from the beginning to the end of the session.
3. The **acceleration distributions** from both sensor locations were compared.
   
This comparison aimed to identify which placement provides the most relevant information for detecting signs of muscular fatigue during jump-rope exercise.

---

## 2. Materials and Methods

### 2.1. Materials

The study was conducted using an **Axivity AX3 tri-axial accelerometer** (Axivity Ltd., United Kingdom), an inertial device widely employed in movement science for the quantification of physical activity.

The AX3 is a standalone data logger that includes:
- a tri-axial MEMS sensor,  
- an internal clock,  
- onboard flash memory enabling continuous data recording.

It connects to a computer via USB for configuration, data transfer, and battery charging.

The sensor was configured with:
- a **sampling frequency of 100 Hz**,  
- a **measurement range of ±8 g**,  

which are suitable parameters for capturing rapid movements such as jump-rope exercise.

The devices were firmly attached to the right wrist and right ankle to minimize motion artifacts. After each exercise bout, the recordings were exported in CSV format using the OmGui software (Axivity Ltd.).

### 2.2. Experimental Protocol

### General Description

The study was conducted with a voluntary female student who presented no known locomotor disorders or functional limitations. She performed a jump-rope exercise at a self-selected intensity for a duration sufficient to induce progressive muscular fatigue.

During all trials, two Axivity AX3 accelerometers were used simultaneously: one on the right wrist and one on the right ankle. This setup allowed us to record, for the same movement and at the same instant, two acceleration signals corresponding to two distinct body segments. The goal was to compare the temporal dynamics of these signals to determine which sensor location is most relevant for detecting indicators of muscular fatigue.

---

### Experimental Conditions


| Sensor                         | Body location | Exercise   | Recording mode |
|-------------------------------|---------------|------------|----------------|
| Axivity AX3, 100 Hz sampling rate | Right wrist   | Jump rope  | Simultaneous   |
| Axivity AX3, 100 Hz sampling rate | Right ankle   | Jump rope  | Simultaneous   |

**Table 1 : Experimental Conditions**

---

### Programming and configuring the sensor:

Before each measurement, the Axivity AX3 sensor was configured using the OmGui software (Axivity Ltd.). This software allows sensors to be set up, initialized, and synchronized prior to data recording.

Here is the website link:[Texte du lien](https://axivity.com/userguides/omgui/)

The configuration steps were as follows:
1. Sensor connection: The sensor is connected to the computer via a micro-USB type B cable. It automatically appears in the Device Browser Pane of the OmGui software.
2. Clearing previous data: The Clear button is used to delete any prior recordings stored in the sensor’s internal memory, ensuring a blank data file for each test.
3. Acquisition parameter settings:
    * Sampling frequency: 100 Hz
    * Measurement range: ±8 g
    * Start mode: Start at programmed time
    * Synchronization: the sensor’s internal clock is automatically adjusted to the computer’s time at validation.
4. Start time programming: The sensor was programmed to automatically begin recording at the predefined time set in the software (interval start time). Once disconnected from the computer, the device remained in standby until the scheduled time was reached, at which point recording started autonomously.

---

### Data Collection and Transfer:

The participant performed three series of jump-rope exercise: the first lasted 4 minutes and the following two lasted 5 minutes each.

A 5-minute rest period was provided between series. This pause allowed the experimenter to: download the recorded data, reprogram the sensors for the next trial, and provide brief muscular recovery before resuming the exercise.

At the end of each series, the accelerometers were reconnected to the computer to retrieve the data. The recording was stopped using the Stop command, then the Download function was used to transfer the file in .CWA format to the OmGui Working Folder.

The recordings were initially saved in the proprietary .CWA binary format, which is not directly compatible with standard data-analysis tools. To process the data in Python, the files were converted into .CSV format using the Export raw data to CSV function in OmGui.

The following export parameters were selected:
- Accelerometer units: Gravity (g), i.e. acceleration expressed in multiples of g (1 g = 9.81 m·s⁻²)
- Timestamp estimation: Formatted (Y–M–D h:m:s.f), providing precise and readable timestamps
- Sub-sampling: disabled, ensuring that the entire raw signal was preserved

The resulting CSV files contained four columns: timestamp, X-axis acceleration, Y-axis acceleration, and Z-axis acceleration. These files were subsequently used for numerical processing, statistical computation (RMS, ENMO, etc.), and graphical visualization in Python.

---

## 3. Measurement Methodology for Acceleration Signals

To assess whether sensor placement (ankle vs. wrist) influences sensitivity to muscle fatigue, we processed the raw triaxial acceleration signals from both locations using the same metric and workflow. The analysis relied on the Euclidean Norm Minus One (ENMO), a widely used index of movement intensity derived from triaxial accelerometer data. ENMO reflects the magnitude of acceleration above 1 g (gravitational acceleration) and therefore quantifies active movement only.

 ### 3.1. Pre-processing of acceleration signals

To ensure consistent processing across both sensor locations, the raw triaxial acceleration data were first combined into a single magnitude representing overall movement intensity. 

$$
\text{Norm} = \sqrt{a_x^2 + a_y^2 + a_z^2}
$$

Movement-related acceleration was then extracted using the Euclidean Norm Minus One (ENMO) metric, which removes the constant gravitational component so that only dynamic motion remains.

$$
\text{ENMO} = \max(\text{Norm} - 1, 0)
$$

Time was normalized for each trial by subtracting the initial timestamp, allowing direct temporal comparison between wrist and ankle recordings.

### 3.2. Sliding-window ENMO integration (10, 20, 30 s)
To examine how movement intensity evolved throughout the exercise, ENMO was integrated over sliding time windows of 10, 20, and 30 seconds. 

$$
\text{ENMO}_{\text{integrated}}(t) = \sum_i \text{ENMO}_i \cdot \Delta t_i
$$

For each window duration, ENMO values were multiplied by the sampling interval and summed over the window, producing a continuous curve that reflects short-term variations in movement dynamics.

$$
\text{ENMO}_{L_s}(t) = \sum_{i = t-L_s}^{t} \text{ENMO}_i \cdot \Delta t_i
$$

These sliding-window curves reveal gradual changes in jump amplitude, impact forces, and coordination that may indicate the onset of muscular fatigue.

### 3.3. Fixed-window ENMO integration (10, 20, 30 s)

To compare corresponding moments of the exercise between the two sensor locations, the ENMO signal was also segmented into non-overlapping fixed windows of 10, 20, and 30 seconds. For each window, total movement intensity was computed, providing one representative value per segment.

$$
\text{ENMO}_{L_s}^{(k)} = \sum_{i \in W_k} \text{ENMO}_i \cdot \Delta t_i,
\qquad
W_k = [kL,\,(k+1)L]
$$

These fixed-window values form a discrete intensity profile, enabling direct ankle–wrist comparison at identical time intervals during the session.

### 3.4. ENMO Boxplot Analysis: Global Distribution Across Sensor Locations

To simplify the overall analysis of the signal, we also represented the data using boxplots. The objective was to obtain a direct and intuitive visualization of the ENMO distribution for each series by comparing the ankle and the wrist on the same graph.
Thus, we produced three separate figures: one for Series 1, one for Series 2, and one for Series 3. Each graph includes two boxplots, one for the ankle sensor and the other for the wrist sensor, which allows for a quick comparison of intensity levels, signal dispersion, and extreme values between the two locations, and highlights the global differences between the sensors across the different series.
