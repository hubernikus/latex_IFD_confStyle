# -*- coding: utf-8 -*-
"""###########################################################################
#
#                   kite validation script
#                     klh   
#
########################################################################### """

# clear all ## To ensure clean workspace
##
# clc close all clear variables

# Import needed libraries
import numpy as np # Basic math library
import yaml # import yaml files

from sys import path

# Import ReadYalm
path.append("/home/lukas/Software/casadi/casadi-py35-np1.9.1-v3.2.3-64bit")
from casadi import *

#create kite model
aircraft = ReadYaml('umx_radian.yaml')
parameters.simulation = 0
parameters.plot = 0
parameters.vr = 0
parameters.int_type = 'cvodes'

start_sample = 10
# s_time = exp_telemetry(start_sample,end)
# f_time = exp_telemetry(end,end)
# parameters.t_span = [s_time, f_time, dt]
# parameters.x0 = exp_telemetry(start_sample,1:13)'
parameters.u0 = [0,0,0]


#
[num, flog, sym] = kite_sim(aircraft, parameters)

##

#check state reconstruction with forward integration
FORWARD_INT = 1
if(FORWARD_INT)
    x0_FI = exp_telemetry(start_sample,7:13)
    log_FI = [x0_FI]
    RB_INT = rigid_body(dt)
    for i = start_sample:length(exp_telemetry)-1
        vb = exp_telemetry(i,1:3)
        wb = exp_telemetry(i,4:6)
        out = RB_INT(struct('x0', x0_FI, 'p', [vb'wb']))
        x0_FI = full(out.xf)
        log_FI = [log_FI x0_FI']
    end
    
    size(log_FI)
    save('forward_simulation_rb.mat', 'log_FI')
else
    load('forward_simulation_rb.mat')
end

## 
# print forward integration results
plot3(exp_telemetry(:,7), exp_telemetry(:,8),-exp_telemetry(:,9))
hold on
plot3(log_FI(:,1), log_FI(:,2), -log_FI(:,3))
axis equal

##

#Extended Kalman Filter test
V = diag([0.010.010.01 0.00010.0050.0050.005].^2)
#W = zeros(13)                                        # model noise
x_est = exp_telemetry(start_sample,1:13)'            # state estimation
e_v = [0.5 0.5 0.5]             #[0.05 0.5 0.1]
e_w = [0.5 0.5 0.5]             #[0.1 0.1 0.5]
e_r = [0.5 0.1 0.1]             #[0.25 0.25 0.05]
e_q = [0.1 0.05 0.05 0.05]    #[0.3 0.05 0.05 0.06]
P_est = 10 * diag([e_v e_w e_r e_q].^2)                 # estimation covariance
W = diag([e_v e_w e_r e_q].^2)

model.num = num
model.sym = sym
model.num.DRE = dre(13, dt)

estim = [x_est']

dyn_func = num.DYN_FUNC
c_time = control(:,1)
points = 3000

p_norms = []
W_est = W
west_log = diag(W_est)
#W = W_est
res_log = []
ctl_log = []
delays = []
x_sim = x_est

rb_model = rigid_body(dt)
rb_model.num.DRE = model.num.DRE

for k = start_sample:start_sample + points - 1
    dt = exp_telemetry(k+1,end) - exp_telemetry(k,end)
    delays = [delaysdt]
    #get corresponding control
    ctl_idx = length(c_time(c_time <= exp_telemetry(k, end)))
    if (isequal(ctl_idx, 0))
        u = [0,0,0]
    else
        u = control(ctl_idx, 2:4)
    end
    ctl_log = [ctl_log, u']
    #get observation
    z_m = exp_telemetry(k+1,7:13)

    #propagate
    #x_sim(2) = x_est(2)
    #out = model.num.INT(struct('x0',x_est, 'p',u))
    #x_est = full(out.xf)
    [x_est, P_est, W_est, res] = kiteEKF(x_est, P_est, u, rb_model, dt, W, V, z_m', parameters.int_type)
    estim = [estim x_est']
    #west_log = [west_log, diag(W_est)]
    res_log = [res_log, res]
    p_norms = [p_norms, norm(real(P_est), 2)]
end

##
idx_plot = start_sample:(start_sample + points)
figure
plot3(exp_telemetry(idx_plot, 7), exp_telemetry(idx_plot, 8), -exp_telemetry(idx_plot, 9))
#plot(exp_telemetry(idx_plot, 7:9), '--')
grid on
hold on
axis equal
#plot(estim(:, 7:9))
plot3(estim(:, 7), estim(:, 8), -estim(:, 9))
title('Measured and Estimated Trajectory')
legend('Measured trajectory','Estimated trajectory')

#attitude
ftime = 0:0.02:(points * 0.02)
figure
plot(exp_telemetry(idx_plot, 10:13),'--')
hold on
grid on
plot(estim(:, 10:13))
title('... Attitude ...')

#linear velocities
figure
plot(ftime', exp_telemetry(idx_plot,1:3),'--')
grid on
hold on
plot(ftime', estim(:,1:3))
title('... Linear Velocities ...')

#angular velocities
size(ftime')
size(exp_telemetry(idx_plot,4:6))
size(estim)
figure
plot(ftime', exp_telemetry(idx_plot,4:6),'--')
grid on
hold on
plot(ftime', estim(:,4:6))
title('... Angular Velocities ...')

#distance from the pivot
figure
dist = sqrt(sum(abs(estim(:,7:9)).^2,2))
dist2 = sqrt(sum(abs(exp_telemetry(idx_plot,7:9)).^2,2))
plot(dist)
grid on
hold on
plot(dist2)
title('... Tether Elongation ...')

#figure
#plot(res_log')
#grid on

#figure
#plot(delays)
#grid on

##
# Check estimation by forward integration

FORWARD_INT = 1
if(FORWARD_INT)
    x0_FI = estim(1,7:13)
    #x0_FI = exp_telemetry(start_sample,7:13)
    log_FI = [x0_FI]
    #dt = mean(dt_log)
    RB_INT = rb_model.INT_RED
    for i = 1:length(estim)-1
    #for i = start_sample:start_sample + points
        vb = estim(i,1:3)
        wb = estim(i,4:6)
        #vb = exp_telemetry(i,1:3)
        #wb = exp_telemetry(i,4:6)
        out = RB_INT(struct('x0', x0_FI, 'p', [vb'wb']))
        x0_FI = full(out.xf)
        log_FI = [log_FI x0_FI']
    end
    
    size(flog)
    size(log_FI)
end

##
# Plot reconstruction results
figure
plot3(exp_telemetry(idx_plot, 7), exp_telemetry(idx_plot, 8), -exp_telemetry(idx_plot, 9))
#plot(exp_telemetry(idx_plot, 10:13))
grid on
hold on
axis equal
# plot(log_FI(:, 4:7),'--')
plot3(log_FI(:, 1), log_FI(:, 2), -log_FI(:, 3))

figure
plot(exp_telemetry(idx_plot, 10:13),'--')
hold on
grid on
plot(log_FI(:, 4:7))