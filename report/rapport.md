# Accelerometer-based measurement to quantify muscle fatigue

**Authors :** Mahoua KONE, Lucie BONNOT, Loubna EL FARESSI, Bomane PEHE 
**Date :** November 10, 2025  
**Supervisor :** Denis MOTTET

---

## 1. Introduction


### Muscular Fatigue and Accelerometry Analysis

Muscular fatigue is characterized by a progressive decline in a muscle’s ability to generate force, manifesting as alterations in movement execution, reduced range of motion, or decreased movement regularity. Although physiological tools such as electromyography, heart rate monitoring, or blood lactate assessment can be used to quantify fatigue, these methods are often costly, invasive, or difficult to implement in real-world conditions.

Inertial sensors, particularly accelerometers, offer a simple, portable, and non-invasive alternative for analyzing movement dynamics. By measuring acceleration along three axes, they provide a quantitative estimation of movement intensity, notably through the acceleration norm.

### Objective of the Study

In this project, we examined the evolution of acceleration signals during a jump-rope exercise. The goal was to determine whether the placement of the sensor influences the ability to detect muscular fatigue throughout the task. Two locations were tested within the same session:

- **Right wrist** — primarily involved in rope rotation  
- **Right ankle** — directly associated with take-off and landing phases

### Working Hypothesis

Our general hypothesis is that the dynamics of the acceleration signal depend on sensor location, as the wrist and ankle are subjected to different biomechanical constraints.

More specifically, we assumed that:

The ankle-mounted sensor would be more sensitive to fatigue-related changes, as it captures variations in propulsion, stability, and impact forces during jumps.

The wrist-mounted sensor would mainly reflect rope rotation, which is expected to be less affected by lower-limb muscular fatigue.

### Data Processing and Analysis

To test this hypothesis:

1. The acceleration signal was analyzed over the full duration of the exercise.
2. The signal was segmented into **normalized time intervals**, allowing us to observe changes in movement intensity from the beginning to the end of the session.
3. The **acceleration distributions** from both sensor locations were compared.
   
This comparison aimed to identify which placement provides the most relevant information for detecting signs of muscular fatigue during jump-rope exercise.

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

### 2.2.1 General Description

The study was conducted with a voluntary female student who presented no known locomotor disorders or functional limitations. She performed a jump-rope exercise at a self-selected intensity for a duration sufficient to induce progressive muscular fatigue.

During all trials, two Axivity AX3 accelerometers were used simultaneously: one on the right wrist and one on the right ankle. This setup allowed us to record, for the same movement and at the same instant, two acceleration signals corresponding to two distinct body segments. The goal was to compare the temporal dynamics of these signals to determine which sensor location is most relevant for detecting indicators of muscular fatigue.

### 2.2.2 Experimental Conditions


| Sensor                         | Body location | Exercise   | Recording mode |
|-------------------------------|---------------|------------|----------------|
| Axivity AX3, 100 Hz sampling rate | Right wrist   | Jump rope  | Simultaneous   |
| Axivity AX3, 100 Hz sampling rate | Right ankle   | Jump rope  | Simultaneous   |

**Table 1 : Experimental Conditions**

### 2.2.3 Programming and configuring the sensor:

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

### 2.2.4 Data Collection and Transfer:

The participant performed three series of jump-rope exercise: the first lasted 4 minutes and the following two lasted 5 minutes each.

A 5-minute rest period was provided between series. This pause allowed the experimenter to: download the recorded data, reprogram the sensors for the next trial, and provide brief muscular recovery before resuming the exercise.

At the end of each series, the accelerometers were reconnected to the computer to retrieve the data. The recording was stopped using the Stop command, then the Download function was used to transfer the file in .CWA format to the OmGui Working Folder.

The recordings were initially saved in the proprietary .CWA binary format, which is not directly compatible with standard data-analysis tools. To process the data in Python, the files were converted into .CSV format using the Export raw data to CSV function in OmGui.

The following export parameters were selected:
- Accelerometer units: Gravity (g), i.e. acceleration expressed in multiples of g (1 g = 9.81 m·s⁻²)
- Timestamp estimation: Formatted (Y–M–D h:m:s.f), providing precise and readable timestamps
- Sub-sampling: disabled, ensuring that the entire raw signal was preserved

The resulting CSV files contained four columns: timestamp, X-axis acceleration, Y-axis acceleration, and Z-axis acceleration. These files were subsequently used for numerical processing, statistical computation (RMS, ENMO, etc.), and graphical visualization in Python.

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

To simplify the overall analysis of the signal, we also represented the data using boxplots. The objective was to obtain a direct and 
intuitive visualization of the ENMO distribution for each series by comparing the ankle and the wrist on the same graph.
Thus, we produced three separate figures: one for Series 1, one for Series 2, and one for Series 3. Each graph includes two boxplots, one for the ankle sensor and the other for the wrist sensor, which allows for a quick comparison of intensity levels, signal dispersion, and extreme values between the two locations, and highlights the global differences between the sensors across the different series.




### 4-3- Boxplot comparison of series 1–3 between ankle and wrist
These three graphs show, for Series 1, 2 and 3 of Trial 2, a comparison of the movements measured at the ankle and at the wrist using boxplots. For each series, the left panel displays the distribution of ENMO values (movement intensity) for both sensor locations, and the right panel shows the distribution of MAD values (signal variability). The boxplots summarize the entire recording: they indicate the overall activity level (position of the median), the spread of values over time (height of the box and length of the whiskers), and the presence of particularly marked movement episodes (extreme points).
These figures therefore make it possible to visualise how movement intensity and variability are distributed between the ankle and the wrist for each series.

[Series 1 – trial 2 ankle vs wrist](data/Series1_trial2_ankle_vs_wrist.png)

**Figure 6: Comparison of ENMO and MAD distributions between the ankle and the wrist in Series 1**

In Series 1, the graphs show ENMO levels (Figure 6) that are overall similar at the ankle and the wrist, suggesting a comparable average movement intensity at both locations. However, the upper part of the ankle boxplot extends higher and contains more extreme values, indicating that the most intense episodes of the trial (sudden movements, impacts, rapid accelerations) occur more frequently or more markedly at the ankle. For MAD, a slightly greater spread is also observed at the ankle, reflecting a signal that is somewhat more unstable and variable over time than at the wrist. In this first condition, the lower limb therefore appears to be slightly more solicited than the upper limb, while the overall activity profile remains relatively balanced between the two sensors.

[Series 2 – trial 2 ankle vs wrist](data/Series2_trial2_ankle_vs_wrist.png)

**Figure 7: Comparison of ENMO and MAD distributions between the ankle and the wrist in Series 2**

In Series 2 (Figure 7), the difference between ankle and wrist is more pronounced than in Series 1. In the ENMO boxplots, the medians are still relatively close, but the ankle box is slightly shifted towards higher values and, more importantly, the ankle shows a much taller column of extreme points than the wrist. This indicates that, even if the average movement intensity is comparable, the most intense movement episodes occur more frequently and more markedly at the ankle. A similar pattern appears for MAD: both the median and the spread are higher for the ankle, with more extreme values than at the wrist. This reflects greater variability in the ankle signal, meaning that accelerations are both stronger and more irregular over time. This profile is consistent with a situation in which the legs produce most of the mechanical work (for example during fast locomotion or frequent changes of pace), while the wrist mainly follows the movement and remains less heavily loaded.

[Series 3 – trial 2 ankle vs wrist](data/Series3_trial2_ankle_vs_wrist.png)

**Figure 8: Comparison of ENMO and MAD distributions between the ankle and the wrist in Series 3**

In contrast with the previous series, in Series 3 the pattern clearly shifts in favour of the wrist. In the ENMO boxplots (Figure 8), wrist values are higher: the median is clearly above that of the ankle, the box is wider, and the column of extreme points extends to much larger values. The ankle, by contrast, remains concentrated around low ENMO values, with few very intense episodes. MAD shows a similar pattern: both the spread and the number of extreme values are greater at the wrist, whereas the ankle displays a more compact distribution centred on low to moderate levels. Taken together, these results suggest that in this condition the strongest and most irregular movements are mainly produced by the upper limb (arm swings, manipulations, trunk movements driving the wrist), while the lower limbs remain relatively stable or follow a more regular movement pattern.
Overall, the three figures show that the relative contribution of the ankle and the wrist to the measured activity varies across series. In Series 1 and 2, ENMO and MAD values are higher at the ankle, indicating a predominance of lower-limb movements. In contrast, in Series 3 these indices are higher at the wrist, reflecting a greater involvement of the upper limb in the activity.




### 5- Discussion












In the present experiment, our results are consistent with these findings. At the ankle, ENMO and MAD clearly decrease across the three series and the highest values become rarer, which is compatible with a progressive loss of lower-limb power during the jump rope task. At the wrist, by contrast, ENMO and MAD remain more stable and generally lower in Series 1 and 2, indicating that this sensor mainly reflects rope rotation rather than the decline in leg performance. Only in Series 3 do the wrist values become relatively higher, not because the upper limb is more fatigued, but because ankle propulsion has dropped so much that wrist movements dominate the remaining signal. Overall, this supports the idea that a sensor placed close to the propulsive segments (ankle) is more sensitive to fatigue than one placed on the upper limb (wrist).

### 6- Conclusion

In this project, we analysed jump-rope acceleration signals recorded simultaneously at the ankle and at the wrist using the ENMO metric and its integrated forms. The results showed a clear decrease in movement intensity and variability at the ankle across successive series, consistent with the development of lower-limb fatigue, whereas the wrist signal remained comparatively stable and mainly reflected rope rotation. Boxplot comparisons confirmed that, in the earlier series, movement intensity is dominated by the ankle, while in the final series the wrist becomes relatively more active as ankle propulsion declines.
These findings support the idea that sensor placement strongly influences the ability of accelerometers to detect muscular fatigue. Ankle-mounted devices appear particularly well suited to monitoring the loss of explosiveness in the lower limbs during jump-rope exercise, whereas wrist-mounted sensors provide complementary information about task execution rather than fatigue itself. Although the study is limited to a single participant and a specific protocol, it illustrates the potential of ENMO-based accelerometry as a simple, non-invasive tool for tracking fatigue-related changes in movement and lays the groundwork for future studies involving larger samples, additional tasks and multimodal fatigue indicators.

### 7- Bibliographie

Bakrania K, Yates T, Rowlands AV, Esliger DW, Bunnewell S, Sanders J, Davies M, Khunti K, Edwardson CL (2016) Intensity Thresholds on Raw Acceleration Data: Euclidean Norm Minus One (ENMO) and Mean Amplitude Deviation (MAD) Approaches. PLoS One 11:e0164045. 
CABARKAPA DV, FRY AC, CABARKAPA D, PARRA ME, HERMES MJ (2022) Impact of accelerometer placement on assessment of vertical jump performance  parameters. JPES 22. 
Flynn JM, Holmes JD, Andrews DM (2004) The effect of localized leg muscle fatigue on tibial impact acceleration. Clinical Biomechanics 19:726–732. 
Marotta L, Scheltinga BL, Middelaar R van, Bramer WM, Beijnum B-JF van, Reenalda J, Buurke JH, Marotta L, Scheltinga BL, Middelaar R van, Bramer WM, Beijnum B-JF van, Reenalda J, Buurke JH (2022) Accelerometer-Based Identification of Fatigue in the Lower Limbs during Cyclical Physical Exercise: A Systematic Review. Sensors 22 Available at: https://www.mdpi.com/1424-8220/22/8/3008 [Accessed November 29, 2025]. 
Sandrey MA, Chang Y-J, McCrory JL (2020) The Effect of Fatigue on Leg Muscle Activation and Tibial Acceleration During a Jumping Task. Journal of Sport Rehabilitation 29:1093–1099.


